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

import mock
from google.datacatalog_connectors.commons_test import utils
from google.datacatalog_connectors.rdbms.scrape import config
from google.datacatalog_connectors.rdbms.scrape.sql_objects import \
    metadata_sql_objects_scraper


class MetadataSQLObjectsScraperTestCase(unittest.TestCase):
    __MODULE_PATH = '{}/..'.format(os.path.dirname(os.path.abspath(__file__)))
    __SCRAPE_PACKAGE = 'google.datacatalog_connectors.rdbms.scrape'

    @mock.patch('{}.sql_objects.'.format(__SCRAPE_PACKAGE) +
                'metadata_sql_object_normalizer.MetadataSQLObjectNormalizer.'
                'normalize')
    def test_scrape_no_sql_objects_should_not_return_metadata(
            self, normalize):  # noqa
        metadata = \
            utils.Utils.convert_json_to_object(self.__MODULE_PATH,
                                               'metadata.json')

        normalize.return_value = metadata

        main_scraper = mock.MagicMock()
        scraper = metadata_sql_objects_scraper.MetadataSQLObjectsScraper(
            main_scraper)

        metadata = scraper.scrape(None,
                                  connection_args={
                                      'host': 'localhost',
                                      'port': 1234
                                  })

        self.assertEqual(0, len(metadata))

    @mock.patch('{}.sql_objects.'.format(__SCRAPE_PACKAGE) +
                'metadata_sql_object_normalizer.MetadataSQLObjectNormalizer.'
                'normalize')
    def test_scrape_should_return_metadata(self, normalize):  # noqa
        sql_objects_config = \
            utils.Utils.convert_json_to_object(self.__MODULE_PATH,
                                               'sql_objects_config.json')
        main_scraper = mock.MagicMock()

        main_scraper.get_metadata_as_dataframe.return_value = \
            utils.Utils.retrieve_dataframe_from_file(
                self.__MODULE_PATH,
                'rdbms_sql_objects_dump.csv')

        normalized_metadata = \
            utils.Utils.convert_json_to_object(self.__MODULE_PATH,
                                               'normalized_sql_objects.json')

        normalize.return_value = normalized_metadata

        scraper = metadata_sql_objects_scraper.MetadataSQLObjectsScraper(
            main_scraper)

        loaded_config = mock.MagicMock(config.Config)

        loaded_config.sql_objects_config = sql_objects_config

        returned_metadata = scraper.scrape(loaded_config,
                                           connection_args={
                                               'host': 'localhost',
                                               'port': 1234
                                           })

        self.assertEqual(2, len(returned_metadata))
        self.assertDictEqual(normalized_metadata,
                             returned_metadata['functions'])
