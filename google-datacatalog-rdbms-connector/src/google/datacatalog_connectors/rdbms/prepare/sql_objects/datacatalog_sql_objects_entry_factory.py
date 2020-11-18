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

from google.datacatalog_connectors.rdbms.scrape import config_constants


class DataCatalogSQLObjectsEntryFactory(BaseEntryFactory):

    def __init__(self, project_id, location_id, metadata_host_server,
                 entry_group_id, sql_objects_config):
        self.__project_id = project_id
        self.__location_id = location_id
        self.__metadata_host_server = metadata_host_server
        self.__entry_group_id = entry_group_id
        self.__sql_objects_config = sql_objects_config

    def make_entry_for_sql_object(self, sql_object_key, sql_object_type,
                                  sql_object_item):
        sql_object_config = self.__sql_objects_config[sql_object_key]

        metadata_def = sql_object_config[
            config_constants.SQL_OBJECT_ITEM_METADATA_DEF_KEY]

        name = metadata_def[config_constants.SQL_OBJECT_ITEM_NAME]

        entry_id = self._format_id(name)
        entry = datacatalog.Entry()

        entry.user_specified_type = sql_object_type
        entry.user_specified_system = self.__entry_group_id

        entry.display_name = self._format_display_name(name)

        sql_object_fields = metadata_def[config_constants.SQL_OBJECT_FIELDS]

        sql_object_fields = self.__filter_entry_model_fields(sql_object_fields)

        self.__set_entry_system_timestamps(entry, sql_object_fields,
                                           sql_object_item)

        self.__set_entry_description(entry, sql_object_fields, sql_object_item)

        entry.name = datacatalog.DataCatalogClient.entry_path(
            self.__project_id, self.__location_id, self.__entry_group_id,
            entry_id)

        entry.linked_resource = '//{}//{}'.format(self.__metadata_host_server,
                                                  entry_id)

        return entry_id, entry

    @classmethod
    def __filter_entry_model_fields(cls, sql_object_fields):
        sql_object_fields = [
            field for field in sql_object_fields
            if field[config_constants.SQL_OBJECT_FIELD_TARGET_MODEL] ==
            config_constants.SQL_OBJECT_ENTRY_MODEL
        ]
        return sql_object_fields

    @classmethod
    def __set_entry_system_timestamps(cls, entry, sql_object_fields,
                                      sql_object_item):
        created_time_name = next([
            field for field in sql_object_fields
            if field[config_constants.SQL_OBJECT_FIELD_TARGET_NAME] ==
            config_constants.SQL_OBJECT_ENTRY_CREATE_TIME
        ], None)
        if created_time_name:
            created_time = sql_object_item.get(created_time_name)

            update_time_name = next([
                field for field in sql_object_fields
                if field[config_constants.SQL_OBJECT_FIELD_TARGET_NAME] ==
                config_constants.SQL_OBJECT_ENTRY_UPDATE_TIME
            ], None)

            update_time = None
            if update_time_name:
                update_time = sql_object_item.get(update_time_name)

            create_time, update_time = \
                cls.__convert_source_system_timestamp_fields(
                    created_time,
                    update_time)

            if create_time and update_time:
                created_timestamp = timestamp_pb2.Timestamp()
                created_timestamp.FromSeconds(create_time)
                entry.source_system_timestamps.create_time = created_timestamp

                updated_timestamp = timestamp_pb2.Timestamp()
                updated_timestamp.FromSeconds(update_time)
                entry.source_system_timestamps.update_time = updated_timestamp

    @classmethod
    def __set_entry_description(cls, entry, sql_object_fields,
                                sql_object_item):
        description_name = next([
            field for field in sql_object_fields
            if field[config_constants.SQL_OBJECT_FIELD_TARGET_NAME] ==
            config_constants.SQL_OBJECT_ENTRY_DESCRIPTION
        ], None)
        if description_name:
            description = sql_object_item.get(description_name)

            if pd.isna(description):
                description = ''

            entry.description = description

    @classmethod
    def __convert_date_value_to_epoch(cls, date_value):
        if pd.notnull(date_value):
            return int(date_value.timestamp())

    @classmethod
    def __convert_source_system_timestamp_fields(cls, raw_create_time,
                                                 raw_update_time):
        create_time = cls.__convert_date_value_to_epoch(raw_create_time)
        if not pd.isnull(raw_update_time):
            update_time = cls.__convert_date_value_to_epoch(raw_update_time)
        else:
            update_time = create_time
        return create_time, update_time
