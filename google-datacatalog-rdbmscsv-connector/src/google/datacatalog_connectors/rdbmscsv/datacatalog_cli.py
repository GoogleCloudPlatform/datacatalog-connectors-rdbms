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


class RDBMSCSV2DatacatalogCli(datacatalog_cli.DatacatalogCli):

    def _get_host_arg(self, args):
        return args.rdbms_host

    def _get_entry_group_id(self, args):
        return args.datacatalog_entry_group_id or args.rdbms_type

    def _get_metadata_definition_path(self):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'config/metadata_definition.json')

    def _parse_args(self, argv):
        parser = argparse.ArgumentParser(
            description='Command line to sync any RDBMS'
            ' metadata to Datacatalog')

        parser.add_argument('--datacatalog-project-id',
                            help='Your Google Cloud project ID',
                            required=True)
        parser.add_argument('--datacatalog-location-id',
                            help='Location ID to be used for your'
                            ' Google Cloud Datacatalog',
                            required=True)
        parser.add_argument('--datacatalog-entry-group-id',
                            help='Entry group ID to be used for your Google '
                            'Cloud Datacatalog')
        parser.add_argument('--rdbms-host',
                            help='Your RDBMS server host',
                            required=True)
        parser.add_argument('--rdbms-type',
                            help='Your RDBMS server type',
                            required=True)
        parser.add_argument('--raw-metadata-csv',
                            help='Your raw metadata as a csv file,'
                            ' can be either a local os GCS '
                            'path',
                            required=True)
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
    RDBMSCSV2DatacatalogCli().run(argv[1:] if len(argv) > 0 else argv)
