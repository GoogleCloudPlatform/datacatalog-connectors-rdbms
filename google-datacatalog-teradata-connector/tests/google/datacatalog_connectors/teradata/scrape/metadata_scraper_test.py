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
from unittest.mock import patch, MagicMock

from google.datacatalog_connectors.commons_test import utils

from google.datacatalog_connectors.teradata.scrape import metadata_scraper


class MetadataScraperTestCase(unittest.TestCase):
    __MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
    __SCRAPE_PACKAGE = 'google.datacatalog_connectors.rdbms.scrape'
    __NORMALIZER_CLASS = '{}.metadata_normalizer.MetadataNormalizer'.format(
        __SCRAPE_PACKAGE)

    @patch('pandas.read_csv')
    @patch('{}.normalize'.format(__NORMALIZER_CLASS))
    def test_scrape_databases_metadata_with_csv_should_return_objects(
            self, normalize, read_csv):  # noqa

        metadata = \
            utils.Utils.convert_json_to_object(
                self.__MODULE_PATH,
                'metadata.json')
        read_csv.return_value = metadata
        normalize.return_value = metadata

        scraper = metadata_scraper.MetadataScraper()
        databases_metadata = scraper.scrape({}, csv_path='csv')

        self.assertEqual(1, len(databases_metadata))

    @patch('teradatasql.connect')
    @patch('teradatasql.TeradataConnection.cursor')
    @patch('{}.normalize'.format(__NORMALIZER_CLASS))
    def test_scrape_databases_metadata_with_credentials_should_return_objects(
            self, normalize, cursor, connect):  # noqa

        metadata = \
            utils.Utils.convert_json_to_object(
                self.__MODULE_PATH,
                'metadata.json')

        cursor.fetchall.return_value = \
            utils.Utils.convert_json_to_object(
                self.__MODULE_PATH,
                'rows.json')
        cursor.description =\
            utils.Utils.convert_json_to_object(
                self.__MODULE_PATH,
                'description.json')

        conn = MagicMock()

        connect.return_value = conn

        conn.cursor.return_value = cursor

        normalize.return_value = metadata

        scraper = metadata_scraper.MetadataScraper()
        databases_metadata = scraper.scrape({},
                                            connection_args={
                                                'host': 'mysql_host',
                                                'user': 'dbc',
                                                'pass': 'dbc'
                                            })

        self.assertEqual(1, len(databases_metadata))
        self.assertEqual(connect.call_count, 1)

    @patch('teradatasql.connect')
    @patch('teradatasql.TeradataConnection.cursor')
    @patch('{}.normalize'.format(__NORMALIZER_CLASS))
    def test_scrape_databases_metadata_on_exception_should_re_raise(
            self, normalize, cursor, connect):  # noqa

        connect.side_effect = Exception('Error when connecting to Server')

        scraper = metadata_scraper.MetadataScraper()
        self.assertRaises(Exception,
                          scraper.scrape, {},
                          connection_args={
                              'host': 'mysql_host',
                              'user': 'dbc',
                              'pass': 'dbc'
                          })

        self.assertEqual(connect.call_count, 1)
        self.assertEqual(normalize.call_count, 0)
