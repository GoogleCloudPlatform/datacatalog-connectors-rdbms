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
from google.datacatalog_connectors.rdbms.prepare.sql_objects import \
    datacatalog_sql_objects_tag_template_factory
from google.cloud import datacatalog


class DataCatalogSQLObjectsTagTemplateFactoryTest(unittest.TestCase):
    __MODULE_PATH = '{}/..'.format(os.path.dirname(os.path.abspath(__file__)))

    __BOOL_TYPE = datacatalog.FieldType.PrimitiveType.BOOL
    __DOUBLE_TYPE = datacatalog.FieldType.PrimitiveType.DOUBLE
    __STRING_TYPE = datacatalog.FieldType.PrimitiveType.STRING

    __PROJECT_ID = 'test_project'
    __LOCATION_ID = 'test_location'
    __ENTRY_GROUP_ID = 'my_entry_group'

    def test_make_tag_template_for_sql_objects(self):
        metadata = \
            utils.Utils.convert_json_to_object(self.__MODULE_PATH,
                                               'metadata_with_sql_objects.json')['sql_objects']
        sql_objects_config = \
            utils.Utils.convert_json_to_object(self.__MODULE_PATH,
                                               'sql_objects_config.json')

        factory = datacatalog_sql_objects_tag_template_factory. \
            DataCatalogSQLObjectsTagTemplateFactory(
                self.__PROJECT_ID,
                self.__LOCATION_ID,
                self.__ENTRY_GROUP_ID,
                metadata,
                sql_objects_config
            )

        tag_template_id, tag_template = \
            factory.make_tag_template_for_sql_objects_metadata()

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
        self.assertEqual('Table Type',
                         tag_template.fields['table_type'].display_name)

        self.assertEqual(
            self.__BOOL_TYPE,
            tag_template.fields['has_primary_key'].type.primitive_type)
        self.assertEqual('Has Primary Key',
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
