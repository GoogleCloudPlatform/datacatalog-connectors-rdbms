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

from google.datacatalog_connectors.rdbms.scrape import\
    metadata_scraper
from .query_assembler import QueryAssembler


class MetadataScraper(metadata_scraper.MetadataScraper):

    def _create_rdbms_connection(self, connection_args):
        # import at the method level, because this flow is conditional
        # if the connector reads from a CSV file, this is not used.
        from mysql.connector import connect  # noqa C6204

        con = connect(database=connection_args['database'],
                      host=connection_args['host'],
                      user=connection_args['user'],
                      password=connection_args['pass'])
        return con

    def _get_query_assembler(self):
        return QueryAssembler()

    def _execute_refresh_query(self, cursor, query):
        cursor.execute(query)
        cursor.fetchall()
