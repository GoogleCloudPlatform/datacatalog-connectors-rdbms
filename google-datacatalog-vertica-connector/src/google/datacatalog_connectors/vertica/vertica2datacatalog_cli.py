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

from google.datacatalog_connectors.rdbms import datacatalog_cli

from . import scrape


class Vertica2DataCatalogCli(datacatalog_cli.DatacatalogCli):

    def _get_host_arg(self, args):
        return args.vertica_host

    def _get_connection_args(self, args):
        return {
            'host': args.vertica_host,
            'user': args.vertica_user,
            'pass': args.vertica_pass
        }

    def _get_entry_group_id(self, args):
        return args.datacatalog_entry_group_id or 'vertica'

    def _get_metadata_scraper(self):
        return scrape.MetadataScraper

    def _get_metadata_definition_path(self):
        return f'{os.path.dirname(os.path.abspath(__file__))}' \
               f'/config/metadata_definition.json'

    def _get_query_path(self, args):
        return f'{os.path.dirname(os.path.abspath(__file__))}' \
               f'/config/metadata_query.sql'

    def _parse_args(self, argv):
        parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter)

        parser.add_argument('--vertica-host', help='Vertica server address')
        parser.add_argument('--vertica-user', help='Vertica username')
        parser.add_argument('--vertica-pass', help='Vertica password')
        parser.add_argument('--raw-metadata-csv',
                            help='Cluster metadata in CSV format, can be'
                            ' either a local file or a GCS Bucket path  (if'
                            ' supplied, the Vertica server credentials are'
                            ' ignored)')
        parser.add_argument('--datacatalog-project-id',
                            help='Google Cloud Project ID',
                            required=True)
        parser.add_argument('--datacatalog-location-id',
                            help='Google Cloud Location ID',
                            required=True)
        parser.add_argument('--datacatalog-entry-group-id',
                            help='Entry group ID to be used for your Google '
                            'Cloud Datacatalog')
        parser.add_argument('--service-account-path',
                            help='Local Service Account path (can be supplied'
                            ' as the GOOGLE_APPLICATION_CREDENTIALS'
                            ' environment variable)')
        parser.add_argument('--enable-monitoring',
                            help='Enables monitoring metrics on the connector')

        return parser.parse_args(argv)


def main():
    argv = sys.argv
    Vertica2DataCatalogCli().run(argv[1:] if len(argv) > 0 else argv)
