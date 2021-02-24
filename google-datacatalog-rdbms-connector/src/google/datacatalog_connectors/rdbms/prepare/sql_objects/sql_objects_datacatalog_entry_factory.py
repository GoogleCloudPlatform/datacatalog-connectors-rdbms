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

from google.cloud import datacatalog
from google.protobuf import timestamp_pb2
import pandas as pd

from google.datacatalog_connectors.commons.prepare.base_entry_factory import \
    BaseEntryFactory
from google.datacatalog_connectors.rdbms.common import constants


class SQLObjectsDataCatalogEntryFactory(BaseEntryFactory):

    def __init__(self, project_id, location_id, entry_resource_url_prefix,
                 entry_group_id, sql_objects_config):
        self.__project_id = project_id
        self.__location_id = location_id
        self.__entry_resource_url_prefix = entry_resource_url_prefix
        self.__entry_group_id = entry_group_id
        self.__sql_objects_config = sql_objects_config

    def make_entry_for_sql_object(self, sql_object_key, sql_object_type,
                                  sql_object_item):
        sql_object_config = self.__sql_objects_config[sql_object_key]

        metadata_def = sql_object_config[
            constants.SQL_OBJECT_ITEM_METADATA_DEF_KEY]

        name = sql_object_item[constants.SQL_OBJECT_ITEM_NAME]

        entry_id = self._format_id(name)
        entry = datacatalog.Entry()

        entry.user_specified_type = sql_object_type
        entry.user_specified_system = self.__entry_group_id

        entry.display_name = self._format_display_name(name)

        sql_object_fields = metadata_def[constants.SQL_OBJECT_FIELDS]

        sql_object_fields = self.__filter_entry_model_fields(sql_object_fields)

        self.__set_entry_system_timestamps(entry, sql_object_fields,
                                           sql_object_item)

        self.__set_entry_description(entry, sql_object_fields, sql_object_item)

        entry.name = datacatalog.DataCatalogClient.entry_path(
            self.__project_id, self.__location_id, self.__entry_group_id,
            entry_id)

        entry.linked_resource = '{}/{}'.format(
            self.__entry_resource_url_prefix, entry_id)

        return entry_id, entry

    @classmethod
    def __filter_entry_model_fields(cls, sql_object_fields):
        sql_object_fields = [
            field for field in sql_object_fields
            if field[constants.SQL_OBJECT_FIELD_TARGET][
                constants.SQL_OBJECT_FIELD_TARGET_MODEL] ==
            constants.SQL_OBJECT_ENTRY_MODEL
        ]
        return sql_object_fields

    @classmethod
    def __set_entry_system_timestamps(cls, entry, sql_object_fields,
                                      sql_object_item):

        created_time_field = cls.__find_sql_object_field(
            sql_object_fields, constants.SQL_OBJECT_ENTRY_CREATE_TIME)

        if created_time_field:
            created_time = cls.__get_sql_object_field_value(
                sql_object_item, created_time_field)

            update_time_field = cls.__find_sql_object_field(
                sql_object_fields, constants.SQL_OBJECT_ENTRY_UPDATE_TIME)

            update_time = None
            if update_time_field:
                update_time = cls.__get_sql_object_field_value(
                    sql_object_item, update_time_field)

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
        description_field = cls.__find_sql_object_field(
            sql_object_fields, constants.SQL_OBJECT_ENTRY_DESCRIPTION)

        if description_field:
            description = sql_object_item.get(
                description_field[constants.SQL_OBJECT_FIELD_TARGET][
                    constants.SQL_OBJECT_FIELD_TARGET_NAME])

            if pd.isna(description):
                description = ''

            entry.description = description

    @classmethod
    def __find_sql_object_field(cls, sql_object_fields, field_name):
        return next(
            iter([
                field for field in sql_object_fields
                if field[constants.SQL_OBJECT_FIELD_TARGET][
                    constants.SQL_OBJECT_FIELD_TARGET_NAME] == field_name
            ]), None)

    @classmethod
    def __get_sql_object_field_value(cls, sql_object_item, field):
        return sql_object_item.get(field[constants.SQL_OBJECT_FIELD_TARGET][
            constants.SQL_OBJECT_FIELD_TARGET_NAME])

    @classmethod
    def __convert_timestamp_value_to_epoch(cls, timestamp_value):
        # In case it is not a valid timestamp field, we ignore it.
        if pd.notnull(timestamp_value) and isinstance(timestamp_value,
                                                      pd.Timestamp):
            return int(timestamp_value.timestamp())

    @classmethod
    def __convert_source_system_timestamp_fields(cls, raw_create_time,
                                                 raw_update_time):
        create_time = cls.__convert_timestamp_value_to_epoch(raw_create_time)
        if not pd.isnull(raw_update_time):
            update_time = cls.__convert_timestamp_value_to_epoch(
                raw_update_time)
        else:
            update_time = create_time
        return create_time, update_time
