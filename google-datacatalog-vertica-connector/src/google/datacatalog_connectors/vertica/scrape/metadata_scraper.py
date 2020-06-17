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

from google.datacatalog_connectors.rdbms.scrape import \
    metadata_scraper
import vertica_python


class MetadataScraper(metadata_scraper.MetadataScraper):

    def _create_rdbms_connection(self, connection_args):
        conn_info = {
            'host': connection_args.get('host'),
            'port': 5433,
            'user': connection_args.get('user'),
            'password': connection_args.get('pass'),

            # connection timeout is not enabled by default
            # 5 seconds timeout for a socket operation
            # (Establishing a TCP connection or read/write operation)
            'connection_timeout': 5
        }

        return vertica_python.connect(**conn_info)
