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

from .. import test_utils
from google.datacatalog_connectors.commons_test import utils
from google.datacatalog_connectors.rdbms.scrape import config
import mock


class QueryAssemblerTestCase(unittest.TestCase):
    __MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
    __SCRAPE_PACKAGE = 'google.datacatalog_connectors.rdbms.scrape'

    @mock.patch('{}.'.format(__SCRAPE_PACKAGE) +
                'metadata_scraper.MetadataNormalizer.' + 'to_metadata_dict')
    @mock.patch('{}.'.format(__SCRAPE_PACKAGE) +
                'query_assembler.QueryAssembler.' +
                'get_refresh_metadata_queries')
    def test_metadata_should_not_be_updated_without_config(
            self, get_refresh_metadata_queries, to_metadata_dict):
        scraper = test_utils.FakeScraper()
        metadata = \
            utils.Utils.convert_json_to_object(self.__MODULE_PATH,
                                               'metadata.json')

        to_metadata_dict.return_value = metadata
        schemas_metadata = scraper.get_metadata({},
                                                connection_args={
                                                    'host': 'localhost',
                                                    'port': 1234
                                                },
                                                user_config=None)

        self.assertEqual(1, len(schemas_metadata))
        self.assertEqual(0, get_refresh_metadata_queries.call_count)

    @mock.patch('{}.'.format(__SCRAPE_PACKAGE) +
                'metadata_scraper.MetadataNormalizer.' + 'to_metadata_dict')
    @mock.patch('{}.'.format(__SCRAPE_PACKAGE) +
                'query_assembler.QueryAssembler.' + 'get_optional_queries')
    def test_optional_metadata_should_not_be_pulled_without_config(
            self, get_optional_queries, to_metadata_dict):
        scraper = test_utils.FakeScraper()
        metadata = \
            utils.Utils.convert_json_to_object(self.__MODULE_PATH,
                                               'metadata.json')

        to_metadata_dict.return_value = metadata
        schemas_metadata = scraper.get_metadata({},
                                                connection_args={
                                                    'host': 'localhost',
                                                    'port': 1234
                                                },
                                                user_config=None)

        self.assertEqual(1, len(schemas_metadata))
        self.assertEqual(0, get_optional_queries.call_count)

    @mock.patch('{}.'.format(__SCRAPE_PACKAGE) +
                'metadata_scraper.MetadataNormalizer.' + 'to_metadata_dict')
    @mock.patch('{}.'.format(__SCRAPE_PACKAGE) +
                'query_assembler.QueryAssembler.' +
                'get_refresh_metadata_queries')
    def test_metadata_should_not_be_updated_with_empty_config(
            self, get_refresh_metadata_queries, to_metadata_dict):
        path_to_empty_config = utils.Utils.get_resolved_file_name(
            self.__MODULE_PATH, 'empty_ingest_cfg.yaml')
        empty_config = config.Config(path_to_empty_config)

        scraper = test_utils.FakeScraper()
        metadata = \
            utils.Utils.convert_json_to_object(self.__MODULE_PATH,
                                               'metadata.json')

        to_metadata_dict.return_value = metadata
        schemas_metadata = scraper.get_metadata({},
                                                connection_args={
                                                    'host': 'localhost',
                                                    'port': 1234
                                                },
                                                user_config=empty_config)
        self.assertEqual(1, len(schemas_metadata))
        self.assertEqual(0, get_refresh_metadata_queries.call_count)

    @mock.patch('{}.'.format(__SCRAPE_PACKAGE) +
                'metadata_scraper.MetadataNormalizer.' + 'to_metadata_dict')
    @mock.patch('{}.'.format(__SCRAPE_PACKAGE) +
                'query_assembler.QueryAssembler.' + 'get_optional_queries')
    def test_optional_metadata_should_not_be_pulled_with_empty_config(
            self, get_optional_queries, to_metadata_dict):
        path_to_empty_config = utils.Utils.get_resolved_file_name(
            self.__MODULE_PATH, 'empty_ingest_cfg.yaml')
        empty_config = config.Config(path_to_empty_config)

        scraper = test_utils.FakeScraper()
        metadata = \
            utils.Utils.convert_json_to_object(self.__MODULE_PATH,
                                               'metadata.json')

        to_metadata_dict.return_value = metadata
        schemas_metadata = scraper.get_metadata({},
                                                connection_args={
                                                    'host': 'localhost',
                                                    'port': 1234
                                                },
                                                user_config=empty_config)
        self.assertEqual(1, len(schemas_metadata))
        self.assertEqual(0, get_optional_queries.call_count)
