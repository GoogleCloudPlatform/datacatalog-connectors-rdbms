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


class MetadataScraper(metadata_scraper.MetadataScraper):

    def _create_rdbms_connection(self, connection_args):
        import cx_Oracle
        con = cx_Oracle.connect(
            connection_args['user'],
            connection_args['pass'],
            '{}:{}/{}'.format(connection_args['host'], connection_args['port'],
                              connection_args['db_service']),
            encoding='UTF-8')
        return con
