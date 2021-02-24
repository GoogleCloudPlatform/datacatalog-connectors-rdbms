#!/usr/bin/python
#
# Copyright 2021 Google LLC
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

    def test_new_instance_valid_schema_should_succeed(self):
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

        config_dict = sql_objects_metadata_config.\
            SQLObjectsMetadataConfig(content)

        self.assertIsNotNone(config_dict)

    def test_new_instance_valid_schema_extra_attributes_should_succeed(self):
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

        config_dict = sql_objects_metadata_config.\
            SQLObjectsMetadataConfig(content)

        self.assertIsNotNone(config_dict)

    def test_new_instance_missing_optional_attributes_should_succeed(self):
        content = '''
        metadata_definition:
          name: 'sp_calculateOrder'
          purpose: 'This stored procedure will calculate orders.'
        '''

        config_dict = sql_objects_metadata_config.\
            SQLObjectsMetadataConfig(content)

        self.assertIsNotNone(config_dict)

    def test_new_instance_invalid_attributes_should_raise(self):
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

        self.assertRaises(schema.SchemaError,
                          sql_objects_metadata_config.SQLObjectsMetadataConfig,
                          content)

    def test_new_instance_invalid_nested_attributes_should_raise(self):
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

        self.assertRaises(schema.SchemaError,
                          sql_objects_metadata_config.SQLObjectsMetadataConfig,
                          content)

    def test_new_instance_missing_attributes_should_raise(self):
        content = '''
        metadata_definition:
          inputs:
            - name: 'in1'
              type: 'string'
          outputs:
            - name: 'out1'
              type: 'int'
        '''

        self.assertRaises(schema.SchemaError,
                          sql_objects_metadata_config.SQLObjectsMetadataConfig,
                          content)

    def test_get_attributes_missing_optional_attributes_should_succeed(self):
        content = '''
        metadata_definition:
          name: 'sp_calculateOrder'
          purpose: 'This stored procedure will calculate orders.'
        '''

        config_dict = sql_objects_metadata_config.\
            SQLObjectsMetadataConfig(content)

        self.assertEqual('sp_calculateOrder', config_dict.get_name())
        self.assertEqual('This stored procedure will calculate orders.',
                         config_dict.get_purpose())
        self.assertIsNone(config_dict.get_inputs_formatted())
        self.assertIsNone(config_dict.get_outputs_formatted())

    def test_get_attributes_valid_schema_should_succeed(self):
        content = '''
        metadata_definition:
          name: 'sp_calculateOrder'
          purpose: 'This stored procedure will calculate orders.'
          inputs:
            - name: 'in1'
              type: 'string'
            - name: 'in2'
              type: 'double'
          outputs:
            - name: 'out1'
              type: 'int'
            - name: 'out2'
              type: 'string'
        '''

        config_dict = sql_objects_metadata_config.\
            SQLObjectsMetadataConfig(content)

        self.assertEqual('sp_calculateOrder', config_dict.get_name())
        self.assertEqual('This stored procedure will calculate orders.',
                         config_dict.get_purpose())
        self.assertEqual('in1 (string), in2 (double)',
                         config_dict.get_inputs_formatted())
        self.assertEqual('out1 (int), out2 (string)',
                         config_dict.get_outputs_formatted())
