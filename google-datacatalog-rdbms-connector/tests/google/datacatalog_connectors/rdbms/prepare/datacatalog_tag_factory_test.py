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
from google.cloud import datacatalog_v1beta1


class DataCatalogTagFactoryTest(unittest.TestCase):

    __MODULE_PATH = os.path.dirname(os.path.abspath(__file__))

    def test_tag_for_table_container_should_set_all_available_fields(  # noqa:E501
            self):  # noqa:E125
        metadata_def = utils.Utils.get_metadata_def_obj(self.__MODULE_PATH)

        factory = datacatalog_tag_factory.DataCatalogTagFactory(metadata_def)

        tag_template = datacatalog_v1beta1.types.TagTemplate()
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

        tag_template = datacatalog_v1beta1.types.TagTemplate()
        tag_template.name = 'template_name'

        schema_dict = {'tables': [{}, {}]}

        tag = factory. \
            make_tag_for_table_container_metadata(tag_template, schema_dict)
        self.assertEqual(2, tag.fields['num_tables'].double_value)

    def test_make_tag_for_table_metadata_should_set_all_available_fields(
            self):  # noqa:E125
        metadata_def = utils.Utils.get_metadata_def_obj(self.__MODULE_PATH)

        factory = datacatalog_tag_factory.DataCatalogTagFactory(metadata_def)

        tag_template = datacatalog_v1beta1.types.TagTemplate()
        tag_template.name = 'template_name'

        tables_dict = {
            'creator': 'creator_test',
            'owner': 'owner_test',
            'update_user': 'update_user_test',
            'num_rows': 5,
            'table_size_mb': 2.0
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
        self.assertEqual(2.0, tag.fields['table_size_mb'].double_value)

    def test_tag_for_table_nan_values_should_set_all_available_fields(  # noqa:E501
            self):  # noqa:E125
        metadata_def = utils.Utils.get_metadata_def_obj(self.__MODULE_PATH)

        factory = datacatalog_tag_factory.DataCatalogTagFactory(metadata_def)

        tag_template = datacatalog_v1beta1.types.TagTemplate()
        tag_template.name = 'template_name'

        tables_dict = {
            'creator': 'creator_test',
            'owner': 'owner_test',
            'update_user': 'update_user_test',
            'num_rows': float('nan'),
            'table_size_mb': float('nan')
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
        self.assertEqual(0, tag.fields['table_size_mb'].double_value)

    def test_make_tag_for_table_metadata_with_database_should_succeed(
            self):  # noqa:E125
        metadata_def = utils.Utils.get_metadata_def_obj(self.__MODULE_PATH)
        metadata_def['database_name'] = 'test_db'

        factory = datacatalog_tag_factory. \
            DataCatalogTagFactory(
                metadata_def
            )

        tag_template = datacatalog_v1beta1.types.TagTemplate()
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

        tag_template = datacatalog_v1beta1.types.TagTemplate()
        tag_template.name = 'template_name'

        tables_dict = {'num_rows': 5}

        tag = factory. \
            make_tag_for_table_metadata(tag_template, tables_dict, 'schema')
        self.assertEqual('schema', tag.fields['schema_name'].string_value)
        self.assertEqual(5, tag.fields['num_rows'].double_value)
