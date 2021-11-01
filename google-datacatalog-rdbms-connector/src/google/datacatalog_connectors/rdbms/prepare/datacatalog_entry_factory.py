#!/usr/bin/python
#
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pandas as pd
from google.cloud import datacatalog
from google.protobuf import timestamp_pb2
from google.datacatalog_connectors.commons.prepare.base_entry_factory import \
    BaseEntryFactory

from google.datacatalog_connectors.rdbms.common import constants


class DataCatalogEntryFactory(BaseEntryFactory):
    NO_VALUE_SPECIFIED = 'UNDEFINED'
    EMPTY_TOKEN = '?'

    def __init__(self, project_id, location_id, entry_resource_url_prefix,
                 entry_group_id, metadata_definition):
        self.__project_id = project_id
        self.__location_id = location_id
        self.__entry_resource_url_prefix = entry_resource_url_prefix
        self.__entry_group_id = entry_group_id
        self.__metadata_definition = metadata_definition

    def make_entries_for_table_container(self, table_container):
        """Create Datacatalog entries from a table container dict.

         :param table_container:
         :return: entry_id, entry
        """

        entry_id = self._format_id(table_container['name'])
        entry = datacatalog.Entry()

        entry.user_specified_type = self.__metadata_definition[
            'table_container_def']['type']
        entry.user_specified_system = self.__entry_group_id

        entry.display_name = self._format_display_name(table_container['name'])

        create_time, update_time = \
            DataCatalogEntryFactory.__convert_source_system_timestamp_fields(
                table_container.get('create_time'),
                table_container.get('update_time'))
        if create_time and update_time:
            created_timestamp = timestamp_pb2.Timestamp()
            created_timestamp.FromSeconds(create_time)
            entry.source_system_timestamps.create_time = created_timestamp

            updated_timestamp = timestamp_pb2.Timestamp()
            updated_timestamp.FromSeconds(update_time)
            entry.source_system_timestamps.update_time = updated_timestamp

        desc = table_container.get('desc')
        if pd.isna(desc):
            desc = ''

        entry.description = desc

        entry.name = datacatalog.DataCatalogClient.entry_path(
            self.__project_id, self.__location_id, self.__entry_group_id,
            entry_id)

        entry.linked_resource = '{}/{}'.format(
            self.__entry_resource_url_prefix, entry_id)

        return entry_id, entry

    def make_entry_for_tables(self, table, table_container_name):
        """Create Datacatalog entries from a table dict.

         :param table:
         :param table_container_name:
         :return: entry_id, entry
        """

        entry_id = self._format_id('{}__{}'.format(table_container_name,
                                                   table['name']))

        entry = datacatalog.Entry()

        # some RDBMS' store views and tables definitions in the same
        # system table, and the name is not user friendly, so we only
        # keep it if it's a VIEW type.
        table_type = table.get(constants.TABLE_TYPE_KEY)
        if table_type and table_type.lower() == \
                constants.VIEW_TYPE_VALUE:

            table_type = table_type.lower()
        else:
            table_type = self.__metadata_definition['table_def']['type']

        entry.user_specified_type = table_type

        entry.user_specified_system = self.__entry_group_id

        entry.display_name = self._format_display_name(table['name'])

        entry.name = datacatalog.DataCatalogClient.entry_path(
            self.__project_id, self.__location_id, self.__entry_group_id,
            entry_id)

        desc = table.get('desc')
        if pd.isna(desc):
            desc = ''

        entry.description = desc

        entry.linked_resource = '{}/{}/{}'.format(
            self.__entry_resource_url_prefix, table_container_name,
            self._format_id(table['name']))

        create_time, update_time = \
            DataCatalogEntryFactory.__convert_source_system_timestamp_fields(
                table.get('create_time'),
                table.get('update_time'))
        if create_time and update_time:
            created_timestamp = timestamp_pb2.Timestamp()
            created_timestamp.FromSeconds(create_time)
            entry.source_system_timestamps.create_time = created_timestamp

            updated_timestamp = timestamp_pb2.Timestamp()
            updated_timestamp.FromSeconds(update_time)
            entry.source_system_timestamps.update_time = updated_timestamp

        columns = []
        for column in table['columns']:
            desc = column.get('desc')
            if pd.isna(desc):
                desc = ''
            columns.append(
                datacatalog.ColumnSchema(
                    column=self._format_id(column['name']),
                    description=desc,
                    type=DataCatalogEntryFactory.__format_entry_column_type(
                        column['type'])))
        entry.schema.columns.extend(columns)

        return entry_id, entry

    @staticmethod
    def __convert_date_value_to_epoch(date_value):
        if pd.notnull(date_value):
            return int(date_value.timestamp())

    @staticmethod
    def __convert_source_system_timestamp_fields(raw_create_time,
                                                 raw_update_time):
        create_time = DataCatalogEntryFactory. \
            __convert_date_value_to_epoch(raw_create_time)
        if not pd.isnull(raw_update_time):
            update_time = DataCatalogEntryFactory. \
                __convert_date_value_to_epoch(raw_update_time)
        else:
            update_time = create_time
        return create_time, update_time

    @staticmethod
    def __format_entry_column_type(source_name):
        if isinstance(source_name, bytes):
            # We've noticed some MySQL instances use bytes-like objects
            # instead of `str` to specify the column types. We are using UTF-8
            # to decode such objects when it happens because UTF-8 is the
            # default character set for MySQL 8.0 onwards.
            #
            # We didn't notice similar behavior with other RDBMS but, if so,
            # we should handle encoding as a configuration option that each
            # RDBMS connector would have to set up. It might be exposed as a
            # CLI arg, so users could easily change that. There is also the
            # option to  scrape that config directly from the DB.
            source_name = source_name.decode("utf-8")

        formatted_name = source_name.replace('&', '_')
        formatted_name = formatted_name.replace(':', '_')
        formatted_name = formatted_name.replace('/', '_')
        formatted_name = formatted_name.replace(' ', '_')

        if formatted_name == DataCatalogEntryFactory.EMPTY_TOKEN:
            formatted_name = DataCatalogEntryFactory.NO_VALUE_SPECIFIED

        return formatted_name
