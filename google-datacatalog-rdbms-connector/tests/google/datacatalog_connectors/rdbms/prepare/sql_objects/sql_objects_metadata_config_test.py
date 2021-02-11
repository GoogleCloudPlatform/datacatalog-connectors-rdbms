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

import unittest

from google.datacatalog_connectors.rdbms.prepare.sql_objects import \
        sql_objects_metadata_config

import schema


class SQLObjectsMetadataConfigTestCase(unittest.TestCase):

    def test_parse_as_dict_valid_schema_should_succeed(self):
        config = sql_objects_metadata_config.SQLObjectsMetadataConfig()

        content = '''
        metadata_definition:
          name: 'sp_calculateOrder'
          purpose: 'This stored procedure will calculate orders.'
          inputs:
            - name: 'in1'
              type: 'string'
          outputs:
            - name: 'out1'
              type: 'int'
        '''

        config_dict = config.parse_as_dict(content)

        self.assertIsNotNone(config_dict)

    def test_parse_as_dict_valid_schema_extra_attributes_should_succeed(self):
        config = sql_objects_metadata_config.SQLObjectsMetadataConfig()

        content = '''
        metadata_definition:
          name: 'sp_calculateOrder'
          purpose: 'This stored procedure will calculate orders.'
          extra: 'unused extra attribute'
          inputs:
            - name: 'in1'
              type: 'string'
          outputs:
            - name: 'out1'
              type: 'int'
        '''

        config_dict = config.parse_as_dict(content)

        self.assertIsNotNone(config_dict)

    def test_parse_as_dict_missing_optional_attributes_should_succeed(self):
        config = sql_objects_metadata_config.SQLObjectsMetadataConfig()

        content = '''
        metadata_definition:
          name: 'sp_calculateOrder'
          purpose: 'This stored procedure will calculate orders.'
        '''

        config_dict = config.parse_as_dict(content)

        self.assertIsNotNone(config_dict)

    def test_parse_as_dict_invalid_attributes_should_raise(self):
        config = sql_objects_metadata_config.SQLObjectsMetadataConfig()

        content = '''
        metadata_definition:
          name: 1231
          purpose: 1233
          inputs:
            - name: 'in1'
              type: 'string'
          outputs:
            - name: 'out1'
              type: 'int'
        '''

        self.assertRaises(schema.SchemaError, config.parse_as_dict, content)

    def test_parse_as_dict_invalid_nested_attributes_should_raise(self):
        config = sql_objects_metadata_config.SQLObjectsMetadataConfig()

        content = '''
        metadata_definition:
          name: 'sp_calculateOrder'
          purpose: 'This stored procedure will calculate orders.'
          inputs:
            - name: 123
              type: 'string'
          outputs:
            - name: 'out1'
              type: 123
        '''

        self.assertRaises(schema.SchemaError, config.parse_as_dict, content)

    def test_parse_as_dict_missing_attributes_should_raise(self):
        config = sql_objects_metadata_config.SQLObjectsMetadataConfig()

        content = '''
        metadata_definition:
          inputs:
            - name: 'in1'
              type: 'string'
          outputs:
            - name: 'out1'
              type: 'int'
        '''

        self.assertRaises(schema.SchemaError, config.parse_as_dict, content)
