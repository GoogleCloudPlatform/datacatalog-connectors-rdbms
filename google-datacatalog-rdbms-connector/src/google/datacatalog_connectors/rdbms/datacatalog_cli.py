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

import abc
from abc import abstractmethod
import json
import logging
import os
import sys

from google.datacatalog_connectors.rdbms.scrape import metadata_scraper, config
from google.datacatalog_connectors.rdbms.sync import \
    datacatalog_synchronizer

ABC = abc.ABCMeta('ABC', (object,), {})  # compatible with Python 2 *and* 3


class DatacatalogCli(ABC):

    def run(self, argv):
        """Runs the command line."""

        args = self._parse_args(argv)
        # Enable logging
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

        if args.service_account_path:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] \
                = args.service_account_path

        self._get_datacatalog_synchronizer()(
            project_id=args.datacatalog_project_id,
            location_id=args.datacatalog_location_id,
            entry_group_id=self._get_entry_group_id(args),
            rbms_host=self._get_host_arg(args),
            metadata_definition=self._metadata_definition(),
            metadata_scraper=self._get_metadata_scraper(),
            connection_args=self._get_connection_args(args),
            query=self._query(args),
            csv_path=args.raw_metadata_csv,
            enable_monitoring=args.enable_monitoring,
            user_config=self._get_user_config()).run()

    def _metadata_definition(self):
        path = self._get_metadata_definition_path()

        with open(path, 'r') as f:
            return json.load(f)

    def _get_datacatalog_synchronizer(self):
        return datacatalog_synchronizer.DataCatalogSynchronizer

    def _get_metadata_scraper(self):
        return metadata_scraper.MetadataScraper

    def _query(self, args):
        if not args.raw_metadata_csv:
            path = self._get_query_path(args)

            with open(path, 'r') as f:
                data = f.read()
                return data

    def _get_user_config(self):
        path = self._get_user_config_path()
        if path:
            user_config = config.Config(path)
            return user_config
        return None

    @abstractmethod
    def _get_metadata_definition_path(self):
        pass

    @abstractmethod
    def _get_host_arg(self, args):
        pass

    @abstractmethod
    def _get_entry_group_id(self, args):
        pass

    @abstractmethod
    def _parse_args(self, argv):
        pass

    def _get_user_config_path(self):
        user_config_path = os.path.join(os.getcwd(), 'ingest_cfg.yaml')
        if os.path.exists(user_config_path):
            return user_config_path
        return None

    # Begin RDBMS connection methods
    def _get_query_path(self, args):
        if not args.raw_metadata_csv:
            raise NotImplementedError(
                'Implementing this method is required to connect to a RDBMS!')

    def _get_connection_args(self, args):
        if not args.raw_metadata_csv:
            raise NotImplementedError(
                'Implementing this method is required to connect to a RDBMS!')

    # End RDBMS connection methods


def main():
    argv = sys.argv
    DatacatalogCli().run(argv[1:] if len(argv) > 0 else argv)
