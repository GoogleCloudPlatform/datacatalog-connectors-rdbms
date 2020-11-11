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
    datacatalog_tag_factory
from google.cloud import datacatalog


class DataCatalogTagFactoryTest(unittest.TestCase):

    __MODULE_PATH = os.path.dirname(os.path.abspath(__file__))

    def test_tag_for_table_container_should_set_all_available_fields(  # noqa:E501
            self):  # noqa:E125
        metadata_def = utils.Utils.get_metadata_def_obj(self.__MODULE_PATH)

        factory = datacatalog_tag_factory.DataCatalogTagFactory(metadata_def)

        tag_template = datacatalog.TagTemplate()
        tag_template.name = 'template_name'

        schema_dict = {
            'creator': 'creator_test',
            'owner': 'owner_test',
            'update_user': 'update_user_test',
            'tables': [{}, {}]
        }

        tag = factory. \
            make_tag_for_table_container_metadata(tag_template, schema_dict)
        self.assertEqual(2, tag.fields['num_tables'].double_value)
        self.assertEqual('creator_test',
                         tag.fields['schema_creator'].string_value)
        self.assertEqual('owner_test', tag.fields['schema_owner'].string_value)
        self.assertEqual('update_user_test',
                         tag.fields['schema_update_user'].string_value)

    def test_tag_for_table_container_missing_fields_should_succeed(  # noqa:E501
            self):  # noqa:E125
        metadata_def = utils.Utils.get_metadata_def_obj(self.__MODULE_PATH)

        factory = datacatalog_tag_factory.DataCatalogTagFactory(metadata_def)

        tag_template = datacatalog.TagTemplate()
        tag_template.name = 'template_name'

        schema_dict = {'tables': [{}, {}]}

        tag = factory. \
            make_tag_for_table_container_metadata(tag_template, schema_dict)
        self.assertEqual(2, tag.fields['num_tables'].double_value)

    def test_make_tag_for_table_metadata_should_set_all_available_fields(
            self):  # noqa:E125
        metadata_def = utils.Utils.get_metadata_def_obj(self.__MODULE_PATH)

        factory = datacatalog_tag_factory.DataCatalogTagFactory(metadata_def)

        tag_template = datacatalog.TagTemplate()
        tag_template.name = 'template_name'

        tables_dict = {
            'creator': 'creator_test',
            'owner': 'owner_test',
            'update_user': 'update_user_test',
            'num_rows': 5,
            'table_size_MB': 2.0
        }

        tag = factory. \
            make_tag_for_table_metadata(tag_template, tables_dict, 'schema')
        self.assertEqual('schema', tag.fields['schema_name'].string_value)
        self.assertEqual('creator_test',
                         tag.fields['table_creator'].string_value)
        self.assertEqual('owner_test', tag.fields['table_owner'].string_value)
        self.assertEqual('update_user_test',
                         tag.fields['table_update_user'].string_value)
        self.assertEqual(5, tag.fields['num_rows'].double_value)
        self.assertEqual(2.0, tag.fields['table_size_MB'].double_value)

    def test_tag_for_table_nan_values_should_set_all_available_fields(  # noqa:E501
            self):  # noqa:E125
        metadata_def = utils.Utils.get_metadata_def_obj(self.__MODULE_PATH)

        factory = datacatalog_tag_factory.DataCatalogTagFactory(metadata_def)

        tag_template = datacatalog.TagTemplate()
        tag_template.name = 'template_name'

        tables_dict = {
            'creator': 'creator_test',
            'owner': 'owner_test',
            'update_user': 'update_user_test',
            'num_rows': float('nan'),
            'table_size_MB': float('nan')
        }

        tag = factory. \
            make_tag_for_table_metadata(tag_template, tables_dict, 'schema')
        self.assertEqual('schema', tag.fields['schema_name'].string_value)
        self.assertEqual('creator_test',
                         tag.fields['table_creator'].string_value)
        self.assertEqual('owner_test', tag.fields['table_owner'].string_value)
        self.assertEqual('update_user_test',
                         tag.fields['table_update_user'].string_value)
        self.assertEqual(0, tag.fields['num_rows'].double_value)
        self.assertEqual(0, tag.fields['table_size_MB'].double_value)

    def test_tag_for_table_zero_values_should_set_all_available_fields(  # noqa:E501
            self):  # noqa:E125
        metadata_def = utils.Utils.get_metadata_def_obj(self.__MODULE_PATH)

        factory = datacatalog_tag_factory.DataCatalogTagFactory(metadata_def)

        tag_template = datacatalog.TagTemplate()
        tag_template.name = 'template_name'

        tables_dict = {
            'creator': 'creator_test',
            'owner': 'owner_test',
            'update_user': 'update_user_test',
            'num_rows': 0,
            'table_size_MB': 0
        }

        tag = factory. \
            make_tag_for_table_metadata(tag_template, tables_dict, 'schema')
        self.assertEqual('schema', tag.fields['schema_name'].string_value)
        self.assertEqual('creator_test',
                         tag.fields['table_creator'].string_value)
        self.assertEqual('owner_test', tag.fields['table_owner'].string_value)
        self.assertEqual('update_user_test',
                         tag.fields['table_update_user'].string_value)
        self.assertEqual(0, tag.fields['num_rows'].double_value)
        self.assertEqual(0, tag.fields['table_size_MB'].double_value)

    def test_make_tag_for_table_metadata_with_database_should_succeed(
            self):  # noqa:E125
        metadata_def = utils.Utils.get_metadata_def_obj(self.__MODULE_PATH)
        metadata_def['database_name'] = 'test_db'

        factory = datacatalog_tag_factory. \
            DataCatalogTagFactory(
                metadata_def
            )

        tag_template = datacatalog.TagTemplate()
        tag_template.name = 'template_name'

        tables_dict = {
            'creator': 'creator_test',
            'owner': 'owner_test',
            'update_user': 'update_user_test',
            'num_rows': 5
        }

        tag = factory. \
            make_tag_for_table_metadata(tag_template, tables_dict, 'schema')
        self.assertEqual('test_db', tag.fields['database_name'].string_value)
        self.assertEqual('schema', tag.fields['schema_name'].string_value)
        self.assertEqual('creator_test',
                         tag.fields['table_creator'].string_value)
        self.assertEqual('owner_test', tag.fields['table_owner'].string_value)
        self.assertEqual('update_user_test',
                         tag.fields['table_update_user'].string_value)
        self.assertEqual(5, tag.fields['num_rows'].double_value)

    def test_make_tag_for_table_metadata_missing_fields_should_succeed(
            self):  # noqa:E125
        metadata_def = utils.Utils.get_metadata_def_obj(self.__MODULE_PATH)

        factory = datacatalog_tag_factory.DataCatalogTagFactory(metadata_def)

        tag_template = datacatalog.TagTemplate()
        tag_template.name = 'template_name'

        tables_dict = {'num_rows': 5}

        tag = factory. \
            make_tag_for_table_metadata(tag_template, tables_dict, 'schema')
        self.assertEqual('schema', tag.fields['schema_name'].string_value)
        self.assertEqual(5, tag.fields['num_rows'].double_value)

    def test_make_tags_for_columns_metadata_should_set_all_available_fields(
            self):  # noqa:E125
        metadata_def = utils.Utils.get_metadata_def_obj(self.__MODULE_PATH)

        factory = datacatalog_tag_factory.DataCatalogTagFactory(metadata_def)

        tag_template = datacatalog.TagTemplate()
        tag_template.name = 'template_name'

        tables_dict = {
            'columns': [
                {
                    'name': 'col_1',
                    'mask': 'TRUE',
                    'mask_expression': 'XXX-XXX-XXX'
                },
                {
                    'name': 'col_2',
                    'mask': 'FALSE'
                }
            ]
        }

        tags = factory. \
            make_tags_for_columns_metadata(tag_template, tables_dict)

        tag_1 = tags[0]
        tag_2 = tags[1]

        self.assertEqual(True, tag_1.fields['mask'].bool_value)
        self.assertEqual('XXX-XXX-XXX', tag_1.fields['mask_expression'].string_value)
        self.assertEqual('col_1', tag_1.column)

        self.assertEqual(False, tag_2.fields['mask'].bool_value)
        self.assertIsNone(tag_2.fields.get('mask_expression'))
        self.assertEqual('col_2', tag_2.column)
