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

from google.datacatalog_connectors.commons_test import utils
from google.datacatalog_connectors.rdbms import datacatalog_cli
from google.datacatalog_connectors.rdbms.common import constants
from google.datacatalog_connectors.rdbms import scrape

import mock


class FakeScraper(scrape.metadata_scraper.MetadataScraper):

    def _create_rdbms_connection(self, connection_args):
        con = mock.Mock()
        cur = mock.Mock()

        self.con = con
        self.cur = cur

        cur.fetchall.return_value = utils.Utils.convert_json_to_object(
            os.path.dirname(os.path.abspath(__file__)), 'rows.json')
        cur.description = utils.Utils.convert_json_to_object(
            os.path.dirname(os.path.abspath(__file__)), 'description.json')
        con.cursor.return_value = cur
        return con

    def _get_query_assembler(self):
        return FakeQueryAssembler()

    def _execute_refresh_query(self, cursor, query):
        pass

    def _get_merged_dataframe(self, old_df, new_df, metadata_definition):
        fake_merged_dataframe = old_df
        return fake_merged_dataframe


class FakeScraperWithMetadataEnricher(FakeScraper):

    def _get_metadata_enricher(self):
        return FakeMetadataEnricher


class FakeScraperWithConError(scrape.metadata_scraper.MetadataScraper):

    def _create_rdbms_connection(self, connection_args):
        con = mock.Mock()
        cur = mock.Mock()
        cur.fetchall.side_effect = Exception('connection error')
        return con, cur


class FakeQueryAssembler(scrape.query_assembler.QueryAssembler):

    def _get_refresh_statement(self, tbl_name):
        return "Fake query for {}".format(tbl_name)

    def _get_path_to_num_rows_query(self):
        resolved_name = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '../test_data/num_rows_query.sql')
        return resolved_name


class FakeMetadataEnricher(scrape.metadata_enricher.MetadataEnricher):

    def enrich(self, scraped_dataframe):
        table_container_name = self._metadata_definition[
            constants.TABLE_CONTAINER_DEF_KEY][constants.ASSET_NAME_KEY]
        table_name = self._metadata_definition[constants.TABLE_DEF_KEY][
            constants.ASSET_NAME_KEY]

        asset_prefix = self._enrich_metadata_dict[
            constants.METADATA_ENRICH_ENTRY_PREFIX]

        scraped_dataframe[
            table_name] = asset_prefix + scraped_dataframe[table_name]
        scraped_dataframe[
            table_container_name] = asset_prefix + scraped_dataframe[
                table_container_name]

        return scraped_dataframe


class FakeCLI(datacatalog_cli.DatacatalogCli):

    def _get_metadata_definition_path(self):
        resolved_name = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '../test_data/metadata_definition.json')
        return resolved_name

    def _get_query_path(self, args):
        resolved_name = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '../test_data/metadata_query.sql')
        return resolved_name

    def _get_connection_args(self, args):
        return {'database': 'test_db'}

    def _get_entry_group_id(self, args):
        return 'rdbms_entry_group_id'

    def _get_user_config_path(self):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            '../test_data/ingest_cfg.yaml')

    def _get_metadata_scraper(self):
        return FakeScraper

    def _parse_args(self, argv):
        args = MockedObject()
        args.datacatalog_project_id = 'project_id'
        args.datacatalog_location_id = 'uscentral-1'
        args.rdbms_host = 'localhost'
        args.entry_resource_url_prefix = 'my_on_prem_system'
        args.raw_metadata_csv = utils.Utils.get_resolved_file_name(
            os.path.dirname(os.path.abspath(__file__)), 'rdbms_full_dump.csv')
        args.service_account_path = 'my_sa.json'
        args.enable_monitoring = True

        return args

    def _get_host_arg(self, args):
        return args.rdbms_host


class MockedObject(object):

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]
