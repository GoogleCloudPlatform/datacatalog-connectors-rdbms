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

import os
import unittest

from google.datacatalog_connectors.commons_test import utils
from google.datacatalog_connectors.rdbms.prepare import \
    datacatalog_tag_template_factory
from google.cloud import datacatalog


class DataCatalogTagTemplateFactoryTest(unittest.TestCase):
    __DOUBLE_TYPE = datacatalog.FieldType.PrimitiveType.DOUBLE
    __STRING_TYPE = datacatalog.FieldType.PrimitiveType.STRING
    __BOOL_TYPE = datacatalog.FieldType.PrimitiveType.BOOL

    __MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
    __PROJECT_ID = 'test_project'
    __LOCATION_ID = 'test_location'
    __ENTRY_GROUP_ID = 'my_entry_group'

    def test_make_tag_template_for_table_container_metadata(self):
        metadata_def = utils.Utils.get_metadata_def_obj(self.__MODULE_PATH)

        factory = datacatalog_tag_template_factory. \
            DataCatalogTagTemplateFactory(
                self.__PROJECT_ID,
                self.__LOCATION_ID,
                self.__ENTRY_GROUP_ID,
                metadata_def
            )
        tag_template_id, tag_template = \
            factory.make_tag_template_for_table_container_metadata()

        self.assertEqual('my_entry_group_schema_metadata', tag_template_id)
        self.assertEqual('My_entry_group Schema - Metadata',
                         tag_template.display_name)

        self.assertEqual(self.__DOUBLE_TYPE,
                         tag_template.fields['num_tables'].type.primitive_type)
        self.assertEqual('Number of tables',
                         tag_template.fields['num_tables'].display_name)

        self.assertEqual(
            self.__STRING_TYPE,
            tag_template.fields['schema_owner'].type.primitive_type)
        self.assertEqual('Schema Owner',
                         tag_template.fields['schema_owner'].display_name)

        self.assertEqual(
            self.__STRING_TYPE,
            tag_template.fields['schema_creator'].type.primitive_type)
        self.assertEqual('Schema Creator',
                         tag_template.fields['schema_creator'].display_name)

        self.assertEqual(
            self.__STRING_TYPE,
            tag_template.fields['schema_update_user'].type.primitive_type)
        self.assertEqual(
            'Schema Last Modified User',
            tag_template.fields['schema_update_user'].display_name)

    def test_make_tag_template_for_table_metadata(self):
        metadata_def = utils.Utils.get_metadata_def_obj(self.__MODULE_PATH)

        factory = datacatalog_tag_template_factory. \
            DataCatalogTagTemplateFactory(
                self.__PROJECT_ID,
                self.__LOCATION_ID,
                self.__ENTRY_GROUP_ID,
                metadata_def
            )
        tag_template_id, tag_template = \
            factory.make_tag_template_for_table_metadata()

        self.assertEqual('my_entry_group_table_metadata', tag_template_id)
        self.assertEqual('My_entry_group Table - Metadata',
                         tag_template.display_name)

        self.assertEqual(
            self.__STRING_TYPE,
            tag_template.fields['schema_name'].type.primitive_type)
        self.assertEqual('Schema Name',
                         tag_template.fields['schema_name'].display_name)

        self.assertEqual(self.__DOUBLE_TYPE,
                         tag_template.fields['num_rows'].type.primitive_type)
        self.assertEqual('Number of rows',
                         tag_template.fields['num_rows'].display_name)

        self.assertEqual(
            self.__STRING_TYPE,
            tag_template.fields['table_creator'].type.primitive_type)
        self.assertEqual('Table Creator',
                         tag_template.fields['table_creator'].display_name)

        self.assertEqual(self.__STRING_TYPE,
                         tag_template.fields['table_type'].type.primitive_type)
        self.assertEqual('Table type',
                         tag_template.fields['table_type'].display_name)

        self.assertEqual(
            self.__BOOL_TYPE,
            tag_template.fields['has_primary_key'].type.primitive_type)
        self.assertEqual('Has primary key',
                         tag_template.fields['has_primary_key'].display_name)

        self.assertEqual(
            self.__STRING_TYPE,
            tag_template.fields['table_owner'].type.primitive_type)
        self.assertEqual('Table Owner',
                         tag_template.fields['table_owner'].display_name)

        self.assertEqual(
            self.__STRING_TYPE,
            tag_template.fields['table_update_user'].type.primitive_type)
        self.assertEqual('Table Last Modified User',
                         tag_template.fields['table_update_user'].display_name)

    def test_make_tag_template_for_column_metadata(self):
        metadata_def = utils.Utils.get_metadata_def_obj(self.__MODULE_PATH)

        factory = datacatalog_tag_template_factory. \
            DataCatalogTagTemplateFactory(
                self.__PROJECT_ID,
                self.__LOCATION_ID,
                self.__ENTRY_GROUP_ID,
                metadata_def
            )
        tag_template_id, tag_template = \
            factory.make_tag_template_for_column_metadata()

        self.assertEqual('my_entry_group_column_metadata', tag_template_id)
        self.assertEqual('My_entry_group Column - Metadata',
                         tag_template.display_name)

        self.assertEqual(self.__BOOL_TYPE,
                         tag_template.fields['masked'].type.primitive_type)
        self.assertEqual('Masked', tag_template.fields['masked'].display_name)

        self.assertEqual(
            self.__STRING_TYPE,
            tag_template.fields['mask_expression'].type.primitive_type)
        self.assertEqual('Mask Expression',
                         tag_template.fields['mask_expression'].display_name)
