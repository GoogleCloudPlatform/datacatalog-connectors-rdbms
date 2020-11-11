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


class DataCatalogTagTemplateFactory(prepare.BaseTagTemplateFactory):

    __DATABASE_TYPE = 'database'
    __BOOL_TYPE = datacatalog.FieldType.PrimitiveType.BOOL
    __DOUBLE_TYPE = datacatalog.FieldType.PrimitiveType.DOUBLE
    __STRING_TYPE = datacatalog.FieldType.PrimitiveType.STRING

    def __init__(self, project_id, location_id, entry_group_id,
                 metadata_definition):
        self.__project_id = project_id
        self.__location_id = location_id
        self.__entry_group_id = entry_group_id
        self.__metadata_definition = metadata_definition

    def make_tag_template_for_table_container_metadata(self):
        """
         Create a Tag Template with technical fields
         for Table Container metadata.
         :return: tag_template_id, tag_template
        """

        tag_template = datacatalog.TagTemplate()

        table_container_type = self.__metadata_definition[
            'table_container_def']['type']
        tag_template_id = '{}_{}_metadata'.format(self.__entry_group_id,
                                                  table_container_type)

        tag_template.name = \
            datacatalog.DataCatalogClient.tag_template_path(
                project=self.__project_id,
                location=self.__location_id,
                tag_template=tag_template_id)

        tag_template.display_name = '{} {} - Metadata'.format(
            self.__entry_group_id.capitalize(),
            table_container_type.capitalize())

        self.__add_creator_field_to_template(table_container_type,
                                             tag_template)
        self.__add_owner_field_to_template(table_container_type, tag_template)
        self.__add_update_user_field_to_template(table_container_type,
                                                 tag_template)

        self._add_primitive_type_field(tag_template, 'num_tables',
                                       self.__DOUBLE_TYPE, 'Number of tables')

        return tag_template_id, tag_template

    def make_tag_template_for_table_metadata(self):
        """Create a Tag Template with technical fields for Table metadata.
         :return: tag_template_id, tag_template
        """

        tag_template = datacatalog.TagTemplate()

        table_type = self.__metadata_definition['table_def']['type']

        tag_template_id = '{}_{}_metadata'.format(self.__entry_group_id,
                                                  table_type)

        tag_template.name = \
            datacatalog.DataCatalogClient.tag_template_path(
                project=self.__project_id,
                location=self.__location_id,
                tag_template=tag_template_id)

        tag_template.display_name = '{} {} - Metadata'.format(
            self.__entry_group_id.capitalize(), table_type.capitalize())

        self.__add_creator_field_to_template(table_type, tag_template)
        self.__add_owner_field_to_template(table_type, tag_template)
        self.__add_update_user_field_to_template(table_type, tag_template)

        table_container_name = self.__metadata_definition[
            'table_container_def']['name']
        table_container_type = self.__metadata_definition[
            'table_container_def']['type']

        self._add_primitive_type_field(
            tag_template, table_container_name, self.__STRING_TYPE,
            '{} Name'.format(table_container_type.capitalize()))

        self.__add_database_name_to_tag_template(tag_template)

        self._add_primitive_type_field(tag_template, 'num_rows',
                                       self.__DOUBLE_TYPE, 'Number of rows')

        self._add_primitive_type_field(tag_template, 'table_size_MB',
                                       self.__DOUBLE_TYPE, 'Table Size in MB')

        self._add_primitive_type_field(tag_template, 'table_type',
                                       self.__STRING_TYPE, 'Table Type')

        self._add_primitive_type_field(tag_template, 'has_primary_key',
                                       self.__BOOL_TYPE, 'Has Primary Key')

        return tag_template_id, tag_template

    def make_tag_template_for_column_metadata(self):
        """Create a Tag Template with technical fields for Column metadata.
         :return: tag_template_id, tag_template
        """

        tag_template = datacatalog.TagTemplate()

        column_type = self.__metadata_definition['column_def']['type']

        tag_template_id = '{}_{}_metadata'.format(self.__entry_group_id,
                                                  column_type)

        tag_template.name = \
            datacatalog.DataCatalogClient.tag_template_path(
                project=self.__project_id,
                location=self.__location_id,
                tag_template=tag_template_id)

        tag_template.display_name = '{} {} - Metadata'.format(
            self.__entry_group_id.capitalize(), column_type.capitalize())

        self._add_primitive_type_field(tag_template, 'masked',
                                       self.__BOOL_TYPE, 'Masked')

        self._add_primitive_type_field(tag_template, 'mask_expression',
                                       self.__STRING_TYPE, 'Mask Expression')

        return tag_template_id, tag_template

    def __add_database_name_to_tag_template(self, tag_template):
        table_container_type = self.__metadata_definition[
            'table_container_def']['type']

        if table_container_type != DataCatalogTagTemplateFactory.\
                __DATABASE_TYPE:
            self._add_primitive_type_field(tag_template, 'database_name',
                                           self.__STRING_TYPE, 'Database name')

    @classmethod
    def __add_creator_field_to_template(cls, attribute_type, tag_template):
        creator_key = '{}_creator'.format(attribute_type)

        cls._add_primitive_type_field(
            tag_template, creator_key, cls.__STRING_TYPE,
            '{} Creator'.format(attribute_type.capitalize()))

    @classmethod
    def __add_owner_field_to_template(cls, attribute_type, tag_template):
        owner_key = '{}_owner'.format(attribute_type)

        cls._add_primitive_type_field(
            tag_template, owner_key, cls.__STRING_TYPE,
            '{} Owner'.format(attribute_type.capitalize()))

    @classmethod
    def __add_update_user_field_to_template(cls, attribute_type, tag_template):
        update_user_key = '{}_update_user'.format(attribute_type)

        cls._add_primitive_type_field(
            tag_template, update_user_key, cls.__STRING_TYPE,
            '{} Last Modified User'.format(attribute_type.capitalize()))
