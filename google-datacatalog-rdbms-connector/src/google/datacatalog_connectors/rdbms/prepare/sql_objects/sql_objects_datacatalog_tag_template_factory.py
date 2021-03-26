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

import logging
import string

from google.cloud import datacatalog

from google.datacatalog_connectors.commons import prepare
from google.datacatalog_connectors.rdbms.common import constants


class SQLObjectsDataCatalogTagTemplateFactory(prepare.BaseTagTemplateFactory):
    __SNAKE_CASE_FIELDS_SEPARATOR = '_'

    __BOOL_TYPE = datacatalog.FieldType.PrimitiveType.BOOL
    __DOUBLE_TYPE = datacatalog.FieldType.PrimitiveType.DOUBLE
    __STRING_TYPE = datacatalog.FieldType.PrimitiveType.STRING
    __TIMESTAMP_TYPE = datacatalog.FieldType.PrimitiveType.TIMESTAMP

    def __init__(self, project_id, location_id, entry_group_id,
                 sql_objects_config):
        self.__project_id = project_id
        self.__location_id = location_id
        self.__entry_group_id = entry_group_id
        self.__sql_objects_config = sql_objects_config

    def make_tag_templates_for_sql_objects_metadata(self,
                                                    sql_objects_metadata):
        """Create a Tag Template with technical fields for SQL Objects metadata.
         :return: tag_templates_dict
        """
        tag_templates_dict = {}
        if sql_objects_metadata:
            for sql_object_key, _ in sql_objects_metadata.items():
                tag_template_id, tag_template = \
                    self.__make_tag_template_for_sql_object_metadata(
                        sql_object_key)
                tag_templates_dict[tag_template_id] = tag_template

        return tag_templates_dict

    def __make_tag_template_for_sql_object_metadata(self, sql_object_key):
        logging.info('\nCreating template for: %s...', sql_object_key)
        sql_object_config = self.__sql_objects_config[sql_object_key]
        metadata_def = sql_object_config[
            constants.SQL_OBJECT_ITEM_METADATA_DEF_KEY]
        sql_object_type = metadata_def[constants.SQL_OBJECT_TYPE]
        tag_template = datacatalog.TagTemplate()
        tag_template_id = '{}_{}_metadata'.format(self.__entry_group_id,
                                                  sql_object_type)
        tag_template.display_name = '{} {} - Metadata'.format(
            self.__capitalize_word(self.__entry_group_id),
            self.__capitalize_word(sql_object_type))
        tag_template.name = \
            datacatalog.DataCatalogClient.tag_template_path(
                project=self.__project_id,
                location=self.__location_id,
                tag_template=tag_template_id)
        sql_object_fields = metadata_def[constants.SQL_OBJECT_FIELDS]

        for sql_object_field in sql_object_fields:
            self.___add_field_for_sql_object_field(sql_object_field,
                                                   tag_template)

        self.___add_predefined_fields(tag_template)

        return tag_template_id, tag_template

    def ___add_field_for_sql_object_field(self, sql_object_item, tag_template):
        sql_object_target = sql_object_item[constants.SQL_OBJECT_FIELD_TARGET]

        sql_object_target_model = sql_object_target[
            constants.SQL_OBJECT_FIELD_TARGET_MODEL]

        # We only create template fields for tag models.
        if constants.SQL_OBJECT_TAG_MODEL == sql_object_target_model:

            sql_object_target_type = sql_object_target[
                constants.SQL_OBJECT_FIELD_TARGET_TYPE]

            if constants.SQL_OBJECT_DOUBLE_FIELD ==\
                    sql_object_target_type:
                field_type = self.__DOUBLE_TYPE
            elif constants.SQL_OBJECT_STRING_FIELD ==\
                    sql_object_target_type:
                field_type = self.__STRING_TYPE
            elif constants.SQL_OBJECT_TIMESTAMP_FIELD ==\
                    sql_object_target_type:
                field_type = self.__TIMESTAMP_TYPE
            elif constants.SQL_OBJECT_BOOLEAN_FIELD ==\
                    sql_object_target_type:
                field_type = self.__BOOL_TYPE
            else:
                raise Exception('Unrecognised field type: {}'.format(
                    sql_object_target_type))

            sql_object_target_name = sql_object_target[
                constants.SQL_OBJECT_FIELD_TARGET_NAME]

            self._add_primitive_type_field(
                tag_template, sql_object_target_name, field_type,
                self.__capitalize_word(sql_object_target_name))

    def ___add_predefined_fields(self, tag_template):
        self._add_primitive_type_field(
            tag_template, constants.SQL_OBJECT_CONFIG_FIELD_NAME,
            self.__STRING_TYPE,
            self.__capitalize_word(constants.SQL_OBJECT_CONFIG_FIELD_NAME))

        self._add_primitive_type_field(
            tag_template, constants.SQL_OBJECT_CONFIG_FIELD_PURPOSE,
            self.__STRING_TYPE,
            self.__capitalize_word(constants.SQL_OBJECT_CONFIG_FIELD_PURPOSE))

        self._add_primitive_type_field(
            tag_template, constants.SQL_OBJECT_CONFIG_FIELD_INPUTS,
            self.__STRING_TYPE,
            self.__capitalize_word(constants.SQL_OBJECT_CONFIG_FIELD_INPUTS))

        self._add_primitive_type_field(
            tag_template, constants.SQL_OBJECT_CONFIG_FIELD_OUTPUTS,
            self.__STRING_TYPE,
            self.__capitalize_word(constants.SQL_OBJECT_CONFIG_FIELD_OUTPUTS))

    @classmethod
    def __capitalize_word(cls, word):
        return string.capwords(
            word.replace(cls.__SNAKE_CASE_FIELDS_SEPARATOR, ' '))
