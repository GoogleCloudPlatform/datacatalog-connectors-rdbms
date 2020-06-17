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
from unittest.mock import patch

from google.datacatalog_connectors.vertica import scrape


class MetadataScraperTest(unittest.TestCase):
    __SCRAPE_PACKAGE = 'google.datacatalog_connectors.vertica.scrape'

    @patch(
        '{}.metadata_scraper.vertica_python.connect'.format(__SCRAPE_PACKAGE))
    def test_create_rdbms_connection_should_provide_connection_info(
            self, mock_connect):  # noqa: E125

        scraper = scrape.MetadataScraper()

        connection_args = {
            'host': 'test-host',
            'user': 'test-user',
            'pass': 'test-pass'
        }

        scraper._create_rdbms_connection(connection_args)

        expected_connection_info = {
            'host': 'test-host',
            'port': 5433,
            'user': 'test-user',
            'password': 'test-pass',
            'connection_timeout': 5
        }

        mock_connect.assert_called_with(**expected_connection_info)
