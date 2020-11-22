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

from google.cloud import datacatalog

import mock

from google.datacatalog_connectors.commons_test import utils
from google.datacatalog_connectors.rdbms.prepare.sql_objects import \
        assembled_sql_objects_entry_factory


class AssembledSQLObjectsEntryFactoryTestCase(unittest.TestCase):
    __MODULE_PATH = '{}/..'.format(os.path.dirname(os.path.abspath(__file__)))

    __PROJECT_ID = 'test_project'
    __LOCATION_ID = 'location_id'
    __ENTRY_GROUP_ID = 'oracle'
    __MOCKED_ENTRY_PATH = 'mocked_entry_path'

    __METADATA_SERVER_HOST = 'metadata_host'
    __PREPARE_PACKAGE = 'google.datacatalog_connectors.rdbms.prepare'

    @mock.patch('{}.sql_objects.datacatalog_sql_objects_tag_factory'
                '.DataCatalogSQLObjectsTagFactory'.format(_PREPARE_PACKAGE))
    @mock.patch('{}.sql_objects.datacatalog_sql_objects_entry_factory'
                '.DataCatalogSQLObjectsEntryFactory'.format(_PREPARE_PACKAGE))
    def setUp(self, mock_entry_factory, mock_tag_factory):
        metadata = \
            utils.Utils.convert_json_to_object(
                self.__MODULE_PATH,
                'metadata_with_sql_objects.json')['sql_objects']
        sql_objects_config = \
            utils.Utils.convert_json_to_object(self.__MODULE_PATH,
                                               'sql_objects_config.json')

        self.__sql_objects_config = sql_objects_config
        self.__metadata = metadata
        self.__entry_factory = mock_entry_factory.return_value
        self.__tag_factory = mock_tag_factory.return_value

        tag_templates_dict = {
            '{}_{}_metadata'.format(self.__ENTRY_GROUP_ID, 'function'):
                datacatalog.TagTemplate(),
            '{}_{}_metadata'.format(self.__ENTRY_GROUP_ID, 'stored_procedure'):
                datacatalog.TagTemplate()
        }

        self.__factory = assembled_sql_objects_entry_factory. \
            AssembledSQLObjectsEntryFactory(
                AssembledSQLObjectsEntryFactoryTestCase.__PROJECT_ID,
                AssembledSQLObjectsEntryFactoryTestCase.__LOCATION_ID,
                AssembledSQLObjectsEntryFactoryTestCase.
                __METADATA_SERVER_HOST,
                AssembledSQLObjectsEntryFactoryTestCase.__ENTRY_GROUP_ID,
                sql_objects_config,
                tag_templates_dict)

    def test_constructor_should_set_instance_attributes(self):
        attrs = self.__factory.__dict__

        self.assertEqual(
            self.__entry_factory, attrs['_AssembledSQLObjectsEntryFactory'
                                        '__datacatalog_entry_factory'])

    def test_make_entries_for_sql_objects_should_create_entries(self):
        entry_factory = self.__entry_factory
        entry_factory.\
            make_entry_for_sql_object.return_value = 'f_entry_id', {}
        entry_factory.\
            make_entry_for_sql_object.return_value = 'sp_entry_id', {}

        tag_factory = self.__tag_factory
        tag_factory.make_tags_for_sql_object.return_value = [{}]

        assembled_entries = self.__factory.make_entries(self.__metadata)

        self.assertEqual(4, len(assembled_entries))
        self.assertEqual(1, len(assembled_entries[0].tags))
        self.assertEqual(1, len(assembled_entries[1].tags))
