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
from google.datacatalog_connectors.oracle.scrape import metadata_scraper


class MetadataScraperTestCase(unittest.TestCase):
    __MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
    __SCRAPE_PACKAGE = 'google.datacatalog_connectors.rdbms.scrape'
    __NORMALIZER_CLASS = '{}.metadata_normalizer.MetadataNormalizer'.format(
        __SCRAPE_PACKAGE)

    @mock.patch('{}.normalize'.format(__NORMALIZER_CLASS))
    def test_scrape_schemas_metadata_with_csv_should_return_objects(
            self, normalize):  # noqa:E125

        metadata = \
            utils.Utils.convert_json_to_object(
                self.__MODULE_PATH,
                'metadata.json')
        normalize.return_value = metadata

        scraper = metadata_scraper.MetadataScraper()
        schemas_metadata = scraper.scrape(
            {},
            csv_path=utils.Utils.get_resolved_file_name(
                self.__MODULE_PATH, 'oracle_full_dump.csv'))

        self.assertEqual(1, len(schemas_metadata))

    @mock.patch('cx_Oracle.connect')
    @mock.patch('{}.normalize'.format(__NORMALIZER_CLASS))
    def test_scrape_schemas_metadata_with_credentials_should_return_objects(
            self, normalize, connect):  # noqa:E125

        metadata = \
            utils.Utils.convert_json_to_object(
                self.__MODULE_PATH,
                'metadata.json')

        con = mock.Mock()

        connect.return_value = con

        cursor = mock.Mock()

        con.cursor.return_value = cursor

        cursor.fetchall.return_value = \
            utils.Utils.convert_json_to_object(
                self.__MODULE_PATH,
                'rows.json')
        cursor.description = \
            utils.Utils.convert_json_to_object(
                self.__MODULE_PATH,
                'description.json')
        normalize.return_value = metadata

        scraper = metadata_scraper.MetadataScraper()
        schemas_metadata = scraper.scrape({},
                                          connection_args={
                                              'db_service': 'db',
                                              'port': 1234,
                                              'host': 'mysql_host',
                                              'user': 'dbc',
                                              'pass': 'dbc'
                                          })
        self.assertEqual(1, len(schemas_metadata))
        self.assertEqual(connect.call_count, 1)

    @mock.patch('cx_Oracle.connect')
    @mock.patch('{}.normalize'.format(__NORMALIZER_CLASS))
    def test_scrape_schemas_metadata_on_exception_should_re_raise(
            self, normalize, connect):  # noqa:E125

        connect.side_effect = Exception('Error when connecting to Server')

        scraper = metadata_scraper.MetadataScraper()
        self.assertRaises(Exception,
                          scraper.scrape, {},
                          connection_args={
                              'db_service': 'db',
                              'port': 1234,
                              'host': 'mysql_host',
                              'user': 'dbc',
                              'pass': 'dbc'
                          })
        self.assertEqual(connect.call_count, 1)
        self.assertEqual(normalize.call_count, 0)
