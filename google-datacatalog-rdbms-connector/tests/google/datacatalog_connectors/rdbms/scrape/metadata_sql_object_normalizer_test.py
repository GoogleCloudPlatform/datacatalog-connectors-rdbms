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
from google.datacatalog_connectors.rdbms.scrape \
    import metadata_sql_object_normalizer


class MetadataSQLObjectNormalizerTestCase(unittest.TestCase):
    __MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
    __SCRAPE_PACKAGE = 'google.datacatalog_connectors.rdbms.scrape'

    def test_normalize_function_sql_object_metadata_with_csv_should_return_objects(self):
        metadata = utils.Utils.retrieve_dataframe_from_file(
            self.__MODULE_PATH, 'rdbms_sql_objects_dump.csv')

        metadata_dict = \
            metadata_sql_object_normalizer.MetadataSQLObjectNormalizer. \
            to_metadata_dict(
                metadata,
                utils.Utils.get_metadata_def_obj(self.__MODULE_PATH,
                                                 'metadata_definition_functions_sql_object.json'))

        self.assertEqual('function', metadata_dict['type'])

        function_1_dict = metadata_dict['items'][0]
        self.assertEqual('CREDIT_MASK', function_1_dict['name'])
        self.assertEqual('SYSTEM', function_1_dict['schema_name']['value'])
        self.assertEqual('tag', function_1_dict['schema_name']['model'])
        self.assertEqual('string', function_1_dict['schema_name']['type'])

        function_2_dict = metadata_dict['items'][1]
        self.assertEqual('CREDIT_MASK_2', function_2_dict['name'])
        self.assertEqual('SYSTEM', function_2_dict['schema_name']['value'])
        self.assertEqual('tag', function_2_dict['schema_name']['model'])
        self.assertEqual('string', function_2_dict['schema_name']['type'])

    def test_normalize_stored_procedure_sql_object_metadata_with_csv_should_return_objects(self):
        metadata = utils.Utils.retrieve_dataframe_from_file(
            self.__MODULE_PATH, 'rdbms_sql_objects_dump.csv')

        metadata_dict = \
            metadata_sql_object_normalizer.MetadataSQLObjectNormalizer. \
            to_metadata_dict(
                metadata,
                utils.Utils.get_metadata_def_obj(
                    self.__MODULE_PATH,
                    'metadata_definition_stored_procedures_sql_object.json'))

        self.assertEqual('stored_procedure', metadata_dict['type'])

        stored_procedure_1_dict = metadata_dict['items'][0]

        self.assertEqual('STORED_PROCEDURE_CREDIT_MASK', stored_procedure_1_dict['name'])
        self.assertEqual('SYSTEM', stored_procedure_1_dict['schema_name']['value'])
        self.assertEqual('tag', stored_procedure_1_dict['schema_name']['model'])
        self.assertEqual('string', stored_procedure_1_dict['schema_name']['type'])
