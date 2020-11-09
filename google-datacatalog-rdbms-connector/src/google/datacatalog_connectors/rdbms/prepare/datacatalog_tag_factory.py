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

from google.datacatalog_connectors.commons import prepare


class DataCatalogTagFactory(prepare.BaseTagFactory):

    __DATABASE_TYPE = 'database'

    def __init__(self, metadata_definition):
        self.__metadata_definition = metadata_definition

    def make_tag_for_table_container_metadata(self, tag_template,
                                              table_container):
        """
         Create Tags for the Table Container technical
          fields that aren't support yet by Datacatalog api.

         :param tag_template: A datacatalog_v1beta1.types.TagTemplate()
         :param table_container:
         :return: tag
        """

        tag = datacatalog.Tag()

        tag.template = tag_template.name

        tables = table_container.get('tables')

        num_tables = 0

        if tables:
            num_tables = len(tables)

        self._set_double_field(tag, 'num_tables', num_tables)

        self.__add_creator_value_to_tag(
            self.__metadata_definition['table_container_def']['type'],
            table_container, tag)
        self.__add_owner_value_to_tag(
            self.__metadata_definition['table_container_def']['type'],
            table_container, tag)
        self.__add_update_user_value_to_tag(
            self.__metadata_definition['table_container_def']['type'],
            table_container, tag)

        return tag

    def make_tag_for_table_metadata(self, tag_template, table,
                                    table_container_name):
        """
         Create Tags for the Table technical fields that
          aren't support yet by Datacatalog api.

         :param tag_template: A datacatalog_v1beta1.types.TagTemplate()
         :param table:
         :param table_container_name:
         :return: tag
        """

        tag = datacatalog.Tag()

        tag.template = tag_template.name

        num_rows = table.get('num_rows')

        if num_rows is not None:
            if pd.isnull(num_rows):
                num_rows = 0
            self._set_double_field(tag, 'num_rows', num_rows)

        table_container_field = self.__metadata_definition[
            'table_container_def']['name']

        self._set_string_field(tag, table_container_field,
                               table_container_name)

        self.__add_database_name_to_tag(tag)
        self.__add_table_size_value_to_tag(table, tag)
        self.__add_creator_value_to_tag(
            self.__metadata_definition['table_def']['type'], table, tag)
        self.__add_owner_value_to_tag(
            self.__metadata_definition['table_def']['type'], table, tag)
        self.__add_update_user_value_to_tag(
            self.__metadata_definition['table_def']['type'], table, tag)

        return tag

    def __add_database_name_to_tag(self, tag):
        table_container_type = self.__metadata_definition[
            'table_container_def']['type']
        if table_container_type != DataCatalogTagFactory.__DATABASE_TYPE:
            database_name = self.__metadata_definition.get('database_name')
            if database_name:
                self._set_string_field(tag, 'database_name', database_name)

    @classmethod
    def __add_table_size_value_to_tag(cls, metadata, tag):
        table_size = metadata.get('table_size_MB')
        if table_size is not None:
            if pd.isnull(table_size):
                table_size = 0
            cls._set_double_field(tag, 'table_size_MB', table_size)

    @classmethod
    def __add_creator_value_to_tag(cls, attribute_type, metadata, tag):
        creator_key = '{}_creator'.format(attribute_type)
        creator = metadata.get('creator')
        if creator:
            cls._set_string_field(tag, creator_key, creator)

    @classmethod
    def __add_owner_value_to_tag(cls, attribute_type, metadata, tag):
        owner_key = '{}_owner'.format(attribute_type)
        owner = metadata.get('owner')
        if owner:
            cls._set_string_field(tag, owner_key, owner)

    @classmethod
    def __add_update_user_value_to_tag(cls, attribute_type, metadata, tag):
        update_user_key = '{}_update_user'.format(attribute_type)
        update_user = metadata.get('update_user')
        if update_user:
            cls._set_string_field(tag, update_user_key, update_user)
