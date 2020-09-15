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
from google.cloud import datacatalog_v1beta1
from google.datacatalog_connectors.commons.prepare.base_entry_factory import \
    BaseEntryFactory


class DataCatalogEntryFactory(BaseEntryFactory):
    NO_VALUE_SPECIFIED = 'UNDEFINED'
    EMPTY_TOKEN = '?'

    def __init__(self, project_id, location_id, metadata_host_server,
                 entry_group_id, metadata_definition):
        self.__project_id = project_id
        self.__location_id = location_id
        self.__metadata_host_server = metadata_host_server
        self.__entry_group_id = entry_group_id
        self.__metadata_definition = metadata_definition

    def make_entries_for_table_container(self, table_container):
        """Create Datacatalog entries from a table container dict.

         :param table_container:
         :return: entry_id, entry
        """

        entry_id = self._format_id(table_container['name'])
        entry = datacatalog_v1beta1.types.Entry()

        entry.user_specified_type = self.__metadata_definition[
            'table_container_def']['type']
        entry.user_specified_system = self.__entry_group_id

        entry.display_name = self._format_display_name(table_container['name'])

        create_time, update_time = \
            DataCatalogEntryFactory.__convert_source_system_timestamp_fields(
                table_container.get('create_time'),
                table_container.get('update_time'))
        if create_time and update_time:
            entry.source_system_timestamps.create_time.seconds = create_time
            entry.source_system_timestamps.update_time.seconds = update_time

        desc = table_container.get('desc')
        if pd.isna(desc):
            desc = ''

        entry.description = desc

        entry.name = datacatalog_v1beta1.DataCatalogClient.entry_path(
            self.__project_id, self.__location_id, self.__entry_group_id,
            entry_id)

        entry.linked_resource = '//{}//{}'.format(self.__metadata_host_server,
                                                  entry_id)

        return entry_id, entry

    def make_entry_for_tables(self, table, table_container_name):
        """Create Datacatalog entries from a table dict.

         :param table:
         :param table_container_name:
         :return: entry_id, entry
        """

        entry_id = self._format_id('{}__{}'.format(table_container_name,
                                                   table['name']))

        entry = datacatalog_v1beta1.types.Entry()

        entry.user_specified_type = self.__metadata_definition['table_def'][
            'type']
        entry.user_specified_system = self.__entry_group_id

        entry.display_name = self._format_display_name(table['name'])

        entry.name = datacatalog_v1beta1.DataCatalogClient.entry_path(
            self.__project_id, self.__location_id, self.__entry_group_id,
            entry_id)

        desc = table.get('desc')
        if pd.isna(desc):
            desc = ''

        entry.description = desc

        entry.linked_resource = '//{}//{}'.format(
            self.__metadata_host_server, self._format_id(table['name']))

        create_time, update_time = \
            DataCatalogEntryFactory.__convert_source_system_timestamp_fields(
                table.get('create_time'),
                table.get('update_time'))
        if create_time and update_time:
            entry.source_system_timestamps.create_time.seconds = create_time
            entry.source_system_timestamps.update_time.seconds = update_time

        columns = []
        for column in table['columns']:
            desc = column.get('desc')
            if pd.isna(desc):
                desc = ''
            columns.append(
                datacatalog_v1beta1.types.ColumnSchema(
                    column=self._format_id(column['name']),
                    description=desc,
                    type=DataCatalogEntryFactory.__format_entry_column_type(
                        column['type']),
                    mode=None))
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
        formatted_name = source_name.replace('&', '_')
        formatted_name = formatted_name.replace(':', '_')
        formatted_name = formatted_name.replace('/', '_')
        formatted_name = formatted_name.replace(' ', '_')

        if formatted_name == DataCatalogEntryFactory.EMPTY_TOKEN:
            formatted_name = DataCatalogEntryFactory.NO_VALUE_SPECIFIED

        return formatted_name
