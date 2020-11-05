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


class DataCatalogTagTemplateFactory:

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

        num_tables_field = datacatalog.TagTemplateField()
        num_tables_field.type.primitive_type = self.__DOUBLE_TYPE
        num_tables_field.display_name = 'Number of tables'
        tag_template.fields['num_tables'] = num_tables_field

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

        table_container_name_field = datacatalog.TagTemplateField()
        table_container_name_field.type.primitive_type = self.__STRING_TYPE
        table_container_name_field.display_name = '{} Name'.format(
                table_container_type.capitalize())
        tag_template.fields[table_container_name] = table_container_name_field

        self.__add_database_name_to_tag_template(tag_template)

        num_rows_field = datacatalog.TagTemplateField()
        num_rows_field.type.primitive_type = self.__DOUBLE_TYPE
        num_rows_field.display_name = 'Number of rows'
        tag_template.fields['num_rows'] = num_rows_field

        table_size_mb_field = datacatalog.TagTemplateField()
        table_size_mb_field.type.primitive_type = self.__DOUBLE_TYPE
        table_size_mb_field.display_name = 'Table Size in MB'
        tag_template.fields['table_size_MB'] = table_size_mb_field

        return tag_template_id, tag_template

    def __add_database_name_to_tag_template(self, tag_template):
        table_container_type = self.__metadata_definition[
            'table_container_def']['type']

        if table_container_type != DataCatalogTagTemplateFactory.\
                __DATABASE_TYPE:
            database_name_field = datacatalog.TagTemplateField()
            database_name_field.type.primitive_type = self.__STRING_TYPE
            database_name_field.display_name = 'Database name'
            tag_template.fields['database_name'] = database_name_field

    @classmethod
    def __add_creator_field_to_template(cls, attribute_type, tag_template):
        creator_key = '{}_creator'.format(attribute_type)

        creator_field = datacatalog.TagTemplateField()
        creator_field.type.primitive_type = cls.__STRING_TYPE
        creator_field.display_name = \
            '{} Creator'.format(attribute_type.capitalize())
        tag_template.fields[creator_key] = creator_field

    @classmethod
    def __add_owner_field_to_template(cls, attribute_type, tag_template):
        owner_key = '{}_owner'.format(attribute_type)

        owner_field = datacatalog.TagTemplateField()
        owner_field.type.primitive_type = cls.__STRING_TYPE
        owner_field.display_name = \
            '{} Owner'.format(attribute_type.capitalize())
        tag_template.fields[owner_key] = owner_field

    @classmethod
    def __add_update_user_field_to_template(cls, attribute_type, tag_template):
        update_user_key = '{}_update_user'.format(attribute_type)

        update_user_field = datacatalog.TagTemplateField()
        update_user_field.type.primitive_type = cls.__STRING_TYPE
        update_user_field.display_name = \
            '{} Last Modified User'.format(attribute_type.capitalize())
        tag_template.fields[update_user_key] = update_user_field

