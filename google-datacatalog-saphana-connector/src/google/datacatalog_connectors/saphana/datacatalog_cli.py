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

import argparse
import os
import sys

from google.datacatalog_connectors.rdbms import\
    datacatalog_cli
from google.datacatalog_connectors.saphana.scrape import metadata_scraper


class SapHana2DatacatalogCli(datacatalog_cli.DatacatalogCli):

    def _get_metadata_scraper(self):
        return metadata_scraper.MetadataScraper

    def _get_host_arg(self, args):
        return args.saphana_host

    def _get_connection_args(self, args):
        return {
            'database': args.saphana_database,
            'host': args.saphana_host,
            'user': args.saphana_user,
            'pass': args.saphana_pass
        }

    def _get_entry_group_id(self, args):
        return args.datacatalog_entry_group_id or 'saphana'

    def _get_metadata_definition_path(self):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'config/metadata_definition.json')

    def _get_query_path(self, args):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'config/metadata_query.sql')

    def _get_connector_config_path(self):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'config')

    def _parse_args(self, argv):
        parser = argparse.ArgumentParser(
            description='Command line to sync SAP Hana '
            'metadata into Google Data Catalog')

        parser.add_argument('--datacatalog-project-id',
                            help='Your Google Cloud project ID',
                            required=True)
        parser.add_argument(
            '--datacatalog-location-id',
            help='Location ID to be used for your Google Data Catalog',
            required=True)
        parser.add_argument('--datacatalog-entry-group-id',
                            help='Entry group ID to be used for your Google '
                            'Data Catalog')
        parser.add_argument(
            '--saphana-host',
            help='Your SAP Hana server host, this is required even'
            ' for the raw_metadata_csv,'
            ' so we are able to map the created entries'
            ' resource with the SAP Hana host',
            required=True)
        parser.add_argument('--saphana-user',
                            help='Your SAP Hana credentials user')
        parser.add_argument('--saphana-pass',
                            help='Your SAP Hana credentials password')
        parser.add_argument('--saphana-database',
                            help='Your SAP Hana database name')
        parser.add_argument(
            '--raw-metadata-csv',
            help='Your raw metadata as a csv file, '
            'can be either a local os GCS '
            'path (If supplied ignores the SAP Hana server credentials)')
        parser.add_argument('--service-account-path',
                            help='Local Service Account path '
                            '(Can be suplied as '
                            'GOOGLE_APPLICATION_CREDENTIALS env '
                            'var)')
        parser.add_argument('--enable-monitoring',
                            help='Enables monitoring metrics on the connector')
        return parser.parse_args(argv)


def main():
    argv = sys.argv
    SapHana2DatacatalogCli().run(argv[1:] if len(argv) > 0 else argv)
