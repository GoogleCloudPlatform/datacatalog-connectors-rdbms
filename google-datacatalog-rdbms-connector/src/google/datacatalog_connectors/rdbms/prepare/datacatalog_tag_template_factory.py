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

from google.cloud import datacatalog_v1beta1


class DataCatalogTagTemplateFactory:

    __DATABASE_TYPE = 'database'
    __BOOL_TYPE = datacatalog_v1beta1.enums.FieldType.PrimitiveType.BOOL
    __DOUBLE_TYPE = datacatalog_v1beta1.enums.FieldType.PrimitiveType.DOUBLE
    __STRING_TYPE = datacatalog_v1beta1.enums.FieldType.PrimitiveType.STRING

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

        tag_template = datacatalog_v1beta1.types.TagTemplate()

        table_container_type = self.__metadata_definition[
            'table_container_def']['type']
        tag_template_id = '{}_{}_metadata'.format(self.__entry_group_id,
                                                  table_container_type)

        tag_template.name = \
            datacatalog_v1beta1.DataCatalogClient.tag_template_path(
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

        tag_template.fields[
            'num_tables'].type.primitive_type = \
            datacatalog_v1beta1.enums.FieldType.PrimitiveType.DOUBLE.value
        tag_template.fields['num_tables'].display_name = 'Number of tables'

        return tag_template_id, tag_template

    def make_tag_template_for_table_metadata(self):
        """Create a Tag Template with technical fields for Table metadata.
         :return: tag_template_id, tag_template
        """

        tag_template = datacatalog_v1beta1.types.TagTemplate()

        table_type = self.__metadata_definition['table_def']['type']

        tag_template_id = '{}_{}_metadata'.format(self.__entry_group_id,
                                                  table_type)

        tag_template.name = \
            datacatalog_v1beta1.DataCatalogClient.tag_template_path(
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

        tag_template.fields[
            table_container_name].type.primitive_type = \
            DataCatalogTagTemplateFactory.__STRING_TYPE
        tag_template.fields[
            table_container_name].display_name = '{} Name'.format(
                table_container_type.capitalize())

        self.__add_database_name_to_tag_template(tag_template)

        tag_template.fields['num_rows'].display_name = 'Number of rows'
        tag_template.fields['num_rows'].type.primitive_type = \
            DataCatalogTagTemplateFactory.__DOUBLE_TYPE

        tag_template.fields['table_size_MB'].display_name = 'Table Size in MB'
        tag_template.fields['table_size_MB'].type.primitive_type = \
            DataCatalogTagTemplateFactory.__DOUBLE_TYPE

        return tag_template_id, tag_template

    def __add_database_name_to_tag_template(self, tag_template):
        table_container_type = self.__metadata_definition[
            'table_container_def']['type']

        if table_container_type != DataCatalogTagTemplateFactory.\
                __DATABASE_TYPE:
            tag_template.fields['database_name'].display_name = 'Database name'
            tag_template.fields['database_name'].type.primitive_type = \
                DataCatalogTagTemplateFactory.__STRING_TYPE

    @classmethod
    def __add_creator_field_to_template(cls, attribute_type, tag_template):
        creator_key = '{}_creator'.format(attribute_type)
        tag_template.fields[
            creator_key].type.primitive_type = \
            DataCatalogTagTemplateFactory.__STRING_TYPE
        tag_template.fields[creator_key].display_name = \
            '{} Creator'.format(attribute_type.capitalize())

    @classmethod
    def __add_owner_field_to_template(cls, attribute_type, tag_template):
        owner_key = '{}_owner'.format(attribute_type)
        tag_template.fields[
            owner_key].type.primitive_type = \
            DataCatalogTagTemplateFactory.__STRING_TYPE
        tag_template.fields[owner_key].display_name = \
            '{} Owner'.format(attribute_type.capitalize())

    @classmethod
    def __add_update_user_field_to_template(cls, attribute_type, tag_template):
        update_user_key = '{}_update_user'.format(attribute_type)
        tag_template.fields[
            update_user_key].type.primitive_type = \
            DataCatalogTagTemplateFactory.__STRING_TYPE
        tag_template.fields[update_user_key].display_name = \
            '{} Last Modified User'.format(attribute_type.capitalize())
