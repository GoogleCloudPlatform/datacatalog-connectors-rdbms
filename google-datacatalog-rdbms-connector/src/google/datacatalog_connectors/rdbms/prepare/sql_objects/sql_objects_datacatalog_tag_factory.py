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

from google.datacatalog_connectors.commons import prepare

from google.datacatalog_connectors.rdbms.scrape import constants


class SQLObjectsDataCatalogTagFactory(prepare.BaseTagFactory):
    __TRUTHS = {1, '1', 't', 'T', 'true', 'True', 'TRUE'}

    def __init__(self, sql_objects_config):
        self.__sql_objects_config = sql_objects_config

    def make_tags_for_sql_object(self, sql_object_key, sql_object_item,
                                 tag_template):
        sql_object_config = self.__sql_objects_config[sql_object_key]

        return [
            self.__make_tag_for_sql_object_metadata(sql_object_config,
                                                    sql_object_item,
                                                    tag_template)
        ]

    def __make_tag_for_sql_object_metadata(self, sql_object_config,
                                           sql_object_item, tag_template):
        tag = datacatalog.Tag()

        tag.template = tag_template.name

        metadata_def = sql_object_config[
            constants.SQL_OBJECT_ITEM_METADATA_DEF_KEY]

        sql_object_fields = metadata_def[constants.SQL_OBJECT_FIELDS]

        for sql_object_field in sql_object_fields:
            self.___add_field_for_sql_object_field(sql_object_field,
                                                   sql_object_item, tag)

        return tag

    def ___add_field_for_sql_object_field(self, sql_object_field,
                                          sql_object_item, tag):
        sql_object_target = sql_object_field[constants.SQL_OBJECT_FIELD_TARGET]

        sql_object_target_model = sql_object_target[
            constants.SQL_OBJECT_FIELD_TARGET_MODEL]

        # We only create template fields for tag models.
        if constants.SQL_OBJECT_TAG_MODEL == sql_object_target_model:

            sql_object_target_type = sql_object_target[
                constants.SQL_OBJECT_FIELD_TARGET_TYPE]

            sql_object_target_name = sql_object_target[
                constants.SQL_OBJECT_FIELD_TARGET_NAME]

            value = sql_object_item[sql_object_target_name]

            if constants.SQL_OBJECT_DOUBLE_FIELD ==\
                    sql_object_target_type:
                if value is None:
                    value = 0
                self._set_double_field(tag, sql_object_target_name, value)
            elif constants.SQL_OBJECT_STRING_FIELD ==\
                    sql_object_target_type:
                self._set_string_field(tag, sql_object_target_name, value)
            elif constants.SQL_OBJECT_TIMESTAMP_FIELD ==\
                    sql_object_target_type:
                self._set_timestamp_field(tag, sql_object_target_name, value)
            elif constants.SQL_OBJECT_BOOLEAN_FIELD ==\
                    sql_object_target_type:
                self._set_bool_field(tag, sql_object_target_name,
                                     self.__convert_to_boolean(value))
            else:
                raise Exception('Unrecognised field type: {}'.format(
                    sql_object_target_type))

    @classmethod
    def __convert_to_boolean(cls, value):
        return value if isinstance(value, bool) else value in cls.__TRUTHS
