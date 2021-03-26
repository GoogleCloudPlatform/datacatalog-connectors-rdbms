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

import mock
import os
import unittest

from google.datacatalog_connectors.commons_test import utils
from google.datacatalog_connectors.rdbms.common import constants
from google.datacatalog_connectors.rdbms.scrape import config


class ConfigTestCase(unittest.TestCase):
    __MODULE_PATH = os.path.dirname(os.path.abspath(__file__))

    @mock.patch('yaml.load')
    def test_config_should_deliver_options_chosen_by_user(self, yaml_load):
        yaml_load.return_value = {
            constants.REFRESH_OPTION: True,
            constants.ROW_COUNT_OPTION: True
        }
        user_config_path = utils.Utils.get_resolved_file_name(
            self.__MODULE_PATH, 'ingest_cfg.yaml')

        connector_config_path = utils.Utils.get_test_config_path(
            self.__MODULE_PATH)

        loaded_config = config.Config(user_config_path, connector_config_path)

        self.assertEqual([constants.ROW_COUNT_OPTION],
                         loaded_config.get_chosen_metadata_options())

    @mock.patch('yaml.load')
    def test_config_should_not_deliver_options_not_chosen_by_user(
            self, yaml_load):
        yaml_load.return_value = {
            constants.REFRESH_OPTION: True,
            constants.ROW_COUNT_OPTION: False
        }
        user_config_path = utils.Utils.get_resolved_file_name(
            self.__MODULE_PATH, 'ingest_cfg.yaml')
        connector_config_path = utils.Utils.get_test_config_path(
            self.__MODULE_PATH)

        loaded_config = config.Config(user_config_path, connector_config_path)

        self.assertEqual([], loaded_config.get_chosen_metadata_options())

    @mock.patch('yaml.load')
    def test_config_no_files_should_not_retrieve_sql_objects(self, yaml_load):
        yaml_load.return_value = {
            constants.SQL_OBJECTS_KEY: [{
                constants.SQL_OBJECT_ITEM_NAME: 'functions_xpto',
                constants.SQL_OBJECT_ITEM_ENABLED_FLAG: True
            }, {
                constants.SQL_OBJECT_ITEM_NAME: 'stored_procedures',
                constants.SQL_OBJECT_ITEM_ENABLED_FLAG: False
            }]
        }

        user_config_path = utils.Utils.get_resolved_file_name(
            self.__MODULE_PATH, 'sql_objects_ingest_cfg.yaml')
        connector_config_path = utils.Utils.get_test_config_path(
            self.__MODULE_PATH)

        loaded_config = config.Config(user_config_path, connector_config_path)

        self.assertEqual(0, len(loaded_config.sql_objects_config))

    @mock.patch('yaml.load')
    def test_config_should_retrieve_sql_objects(self, yaml_load):
        yaml_load.return_value = {
            constants.SQL_OBJECTS_KEY: [{
                constants.SQL_OBJECT_ITEM_NAME: 'functions',
                constants.SQL_OBJECT_ITEM_ENABLED_FLAG: True
            }, {
                constants.SQL_OBJECT_ITEM_NAME: 'stored_procedures',
                constants.SQL_OBJECT_ITEM_ENABLED_FLAG: False
            }]
        }

        user_config_path = utils.Utils.get_resolved_file_name(
            self.__MODULE_PATH, 'sql_objects_ingest_cfg.yaml')
        connector_config_path = utils.Utils.get_test_config_path(
            self.__MODULE_PATH)

        loaded_config = config.Config(user_config_path, connector_config_path)

        self.assertEqual(1, len(loaded_config.sql_objects_config))
        self.assertEqual(
            'functions', loaded_config.sql_objects_config['functions'][
                constants.SQL_OBJECT_ITEM_NAME])
        self.assertIsNotNone(loaded_config.sql_objects_config['functions'][
            constants.SQL_OBJECT_ITEM_QUERY_KEY])

        self.assertIsNotNone(loaded_config.sql_objects_config['functions'][
            constants.SQL_OBJECT_ITEM_METADATA_DEF_KEY])

    @mock.patch('yaml.load')
    def test_config_should_retrieve_base_metadata_query(self, yaml_load):
        yaml_load.return_value = {
            constants.BASE_METADATA_QUERY_FILENAME: 'my_override_query.sql'
        }

        user_config_path = utils.Utils.get_resolved_file_name(
            self.__MODULE_PATH, 'base_metadata_query_ingest_cfg.yaml')
        connector_config_path = utils.Utils.get_test_config_path(
            self.__MODULE_PATH)

        loaded_config = config.Config(user_config_path, connector_config_path)

        self.assertEqual('SELECT  * from db',
                         loaded_config.base_metadata_query)
