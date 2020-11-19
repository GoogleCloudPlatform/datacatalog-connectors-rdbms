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
    datacatalog_sql_objects_tag_factory

from google.datacatalog_connectors.rdbms.scrape import config_constants

from google.cloud import datacatalog


class DataCatalogSQLObjectsTagFactoryTestCase(unittest.TestCase):

    __MODULE_PATH = '{}/..'.format(os.path.dirname(os.path.abspath(__file__)))

    def test_tag_for_function_sql_object_should_set_all_available_fields(  # noqa:E501
            self):  # noqa:E125
        metadata = \
            utils.Utils.convert_json_to_object(
                self.__MODULE_PATH,
                'metadata_with_sql_objects.json')['sql_objects']
        sql_objects_config = \
            utils.Utils.convert_json_to_object(self.__MODULE_PATH,
                                               'sql_objects_config.json')
        factory = datacatalog_sql_objects_tag_factory.\
            DataCatalogSQLObjectsTagFactory(sql_objects_config)

        tag_template = datacatalog.TagTemplate()
        tag_template.name = 'template_name'

        sql_object_key = 'functions'
        sql_object_item = metadata[sql_object_key][
            config_constants.SQL_OBJECT_ITEMS_KEY][0]

        tag = factory. \
            make_tags_for_sql_object(
                sql_object_key, sql_object_item, tag_template)

        self.assertEqual(tag_template.name, tag.template)
        self.assertEqual(
            'CREATE FUNCTION credit_mask(input varchar(19))'
            ' RETURNS output VARCHAR(19)'
            ' LANGUAGE SQLSCRIPT \\nAS\\nBEGIN\\noutput = LEFT(:input,4) ||'
            ' \'-XXXX-XXXX-\' || RIGHT(:input,4);\\nEND',
            tag.fields['definition'].string_value)
        self.assertEqual(1.0, tag.fields['input_parameter_count'].double_value)
        self.assertEqual(True, tag.fields['is_valid'].bool_value)
        self.assertEqual('SYSTEM', tag.fields['owner_name'].string_value)
        self.assertEqual(1.0, tag.fields['return_value_count'].double_value)
        self.assertEqual('SYSTEM', tag.fields['schema_name'].string_value)

    def test_tag_for_stored_procedure_sql_object_should_set_all_available_fields(  # noqa:E501
            self):  # noqa:E125
        metadata = \
            utils.Utils.convert_json_to_object(
                self.__MODULE_PATH,
                'metadata_with_sql_objects.json')['sql_objects']
        sql_objects_config = \
            utils.Utils.convert_json_to_object(self.__MODULE_PATH,
                                               'sql_objects_config.json')
        factory = datacatalog_sql_objects_tag_factory.\
            DataCatalogSQLObjectsTagFactory(sql_objects_config)

        tag_template = datacatalog.TagTemplate()
        tag_template.name = 'template_name'

        sql_object_key = 'stored_procedures'
        sql_object_item = metadata[sql_object_key][
            config_constants.SQL_OBJECT_ITEMS_KEY][0]

        tag = factory. \
            make_tags_for_sql_object(sql_object_key,
                                     sql_object_item, tag_template)

        self.assertEqual(tag_template.name, tag.template)
        self.assertEqual(
            'CREATE FUNCTION credit_mask(input varchar(19))'
            ' RETURNS output VARCHAR(19)'
            ' LANGUAGE SQLSCRIPT \\nAS\\nBEGIN\\noutput = LEFT(:input,4) ||'
            ' \'-XXXX-XXXX-\' || RIGHT(:input,4);\\nEND',
            tag.fields['definition'].string_value)
        self.assertEqual(0.0, tag.fields['input_parameter_count'].double_value)
        self.assertEqual(False, tag.fields['is_valid'].bool_value)
        self.assertEqual('SYSTEM', tag.fields['owner_name'].string_value)
        self.assertEqual(1.0, tag.fields['return_value_count'].double_value)
        self.assertEqual('SYSTEM', tag.fields['schema_name'].string_value)
