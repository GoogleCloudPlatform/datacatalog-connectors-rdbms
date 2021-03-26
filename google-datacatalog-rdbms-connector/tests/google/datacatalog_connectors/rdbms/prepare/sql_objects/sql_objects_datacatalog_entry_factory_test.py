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
from google.datacatalog_connectors.rdbms.common import constants
from google.datacatalog_connectors.rdbms.prepare import sql_objects


class DataCatalogSQLObjectsEntryFactoryTestCase(unittest.TestCase):
    __MODULE_PATH = '{}/..'.format(os.path.dirname(os.path.abspath(__file__)))

    __PROJECT_ID = 'test_project'
    __LOCATION_ID = 'location_id'
    __METADATA_SERVER_HOST = 'metadata_host'
    __ENTRY_GROUP_ID = 'sql_database'

    def test_make_entry_for_function_sql_object_should_set_all_available_fields(  # noqa:E501
            self):  # noqa:E125
        metadata = \
            utils.Utils.convert_json_to_object(
                self.__MODULE_PATH,
                'metadata_with_sql_objects.json')['sql_objects']
        sql_objects_config = \
            utils.Utils.convert_json_to_object(self.__MODULE_PATH,
                                               'sql_objects_config.json')
        factory = sql_objects.\
            SQLObjectsDataCatalogEntryFactory(
                self.__PROJECT_ID,
                self.__LOCATION_ID,
                self.__METADATA_SERVER_HOST,
                self.__ENTRY_GROUP_ID,
                sql_objects_config)

        sql_object_key = 'functions'
        sql_object_type = 'function'
        sql_object_item = metadata[sql_object_key][
            constants.SQL_OBJECT_ITEMS_KEY][0]

        entry_id, entry = factory. \
            make_entry_for_sql_object(
                sql_object_key, sql_object_type, sql_object_item)

        self.assertEqual('CREDIT_MASK', entry_id)
        self.assertEqual('CREDIT_MASK', entry.display_name)
        self.assertEqual(
            'projects/test_project/locations/location_id/'
            'entryGroups/sql_database/entries/CREDIT_MASK', entry.name)
        self.assertEqual('CREDIT_MASK', entry.display_name)
        self.assertEqual('sql_database', entry.user_specified_system)
        self.assertEqual('function', entry.user_specified_type)
        self.assertEqual('metadata_host/CREDIT_MASK', entry.linked_resource)
        self.assertEqual('2020-11-10 16:53:52+00:00',
                         str(entry.source_system_timestamps.create_time))
        self.assertEqual('2020-11-10 16:53:52+00:00',
                         str(entry.source_system_timestamps.update_time))

    def test_make_entry_for_stored_procedure_sql_object_should_set_all_available_fields(  # noqa:E501
            self):  # noqa:E125
        metadata = \
            utils.Utils.convert_json_to_object(
                self.__MODULE_PATH,
                'metadata_with_sql_objects.json')['sql_objects']
        sql_objects_config = \
            utils.Utils.convert_json_to_object(self.__MODULE_PATH,
                                               'sql_objects_config.json')

        factory = sql_objects.\
            SQLObjectsDataCatalogEntryFactory(
                self.__PROJECT_ID,
                self.__LOCATION_ID,
                self.__METADATA_SERVER_HOST,
                self.__ENTRY_GROUP_ID,
                sql_objects_config)

        sql_object_key = 'stored_procedures'
        sql_object_type = 'stored_procedure'
        sql_object_item = metadata[sql_object_key][
            constants.SQL_OBJECT_ITEMS_KEY][0]

        entry_id, entry = factory. \
            make_entry_for_sql_object(
                sql_object_key, sql_object_type, sql_object_item)

        self.assertEqual('CREDIT_MASK', entry_id)
        self.assertEqual('CREDIT_MASK', entry.display_name)
        self.assertEqual(
            'projects/test_project/locations/location_id/'
            'entryGroups/sql_database/entries/CREDIT_MASK', entry.name)
        self.assertEqual('CREDIT_MASK', entry.display_name)
        self.assertEqual('sql_database', entry.user_specified_system)
        self.assertEqual('stored_procedure', entry.user_specified_type)
        self.assertEqual('metadata_host/CREDIT_MASK', entry.linked_resource)
        self.assertEqual('2020-11-10 16:53:52+00:00',
                         str(entry.source_system_timestamps.create_time))
        self.assertEqual('2020-11-10 16:53:52+00:00',
                         str(entry.source_system_timestamps.update_time))
