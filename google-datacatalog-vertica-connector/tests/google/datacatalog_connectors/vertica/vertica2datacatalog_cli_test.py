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
from unittest import mock

from google.datacatalog_connectors import vertica
from google.datacatalog_connectors.vertica import scrape
from google.datacatalog_connectors.vertica import vertica2datacatalog_cli


class Vertica2DataCatalogCliTest(unittest.TestCase):

    def setUp(self):
        self.__cli = vertica2datacatalog_cli.Vertica2DataCatalogCli()

    def test_get_host_arg_should_read_input_args(self):
        args = DictWithAttributeAccess()
        args['vertica_host'] = 'test-host'

        self.assertEqual('test-host', self.__cli._get_host_arg(args))

    def test_get_connection_args_should_read_input_args(self):
        args = DictWithAttributeAccess()
        args['vertica_host'] = 'test-host'
        args['vertica_user'] = 'test-user'
        args['vertica_pass'] = 'test-pass'

        expected_connection_args = {
            'host': 'test-host',
            'user': 'test-user',
            'pass': 'test-pass'
        }

        self.assertEqual(expected_connection_args,
                         self.__cli._get_connection_args(args))

    def test_get_entry_group_id_should_return_value(self):
        args = DictWithAttributeAccess()
        args['datacatalog_entry_group_id'] = 'entry-group'
        self.assertEqual('entry-group', self.__cli._get_entry_group_id(args))

    def test_get_entry_group_id_should_return_vertica_when_missing(self):
        args = DictWithAttributeAccess()
        args['datacatalog_entry_group_id'] = None
        self.assertEqual('vertica', self.__cli._get_entry_group_id(args))

    def test_get_metadata_scraper_should_return_vertica_scraper(self):
        self.assertEqual(scrape.MetadataScraper,
                         self.__cli._get_metadata_scraper())

    @mock.patch('google.datacatalog_connectors.vertica'
                '.vertica2datacatalog_cli.argparse.ArgumentParser')
    def test_parse_args_should_use_builtin_argument_parser(self, mock_parser):
        self.__cli._parse_args({})
        mock_parser.return_value.parse_args.assert_called_once()

    @mock.patch('google.datacatalog_connectors.vertica'
                '.vertica2datacatalog_cli.Vertica2DataCatalogCli')
    def test_main_should_call_cli_run(self, mock_cli):
        vertica.main()
        mock_cli.return_value.run.assert_called_once()


class DictWithAttributeAccess(dict):

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value
