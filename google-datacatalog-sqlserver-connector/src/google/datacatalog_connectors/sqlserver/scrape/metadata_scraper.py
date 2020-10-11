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

from google.datacatalog_connectors.sqlserver.scrape import \
    metadata_enricher

import pandas as pd


class MetadataScraper(metadata_scraper.MetadataScraper):

    # PYODBC return rows as tuples, so we need to convert it to a list,
    # for other RDBMS there is no need to override this function.
    def _create_dataframe(self, rows):
        return pd.DataFrame(map(list, rows))

    def _create_rdbms_connection(self, connection_args):
        # import at the method level, because this flow is conditional
        # if the connector reads from a CSV file, this is not used.
        from pyodbc import connect
        con = connect(
            self.__build_connection(database=connection_args['database'],
                                    host=connection_args['host'],
                                    user=connection_args['user'],
                                    password=connection_args['pass']))
        return con

    @classmethod
    def __build_connection(cls, database, host, user, password):
        return 'DRIVER={ODBC Driver 17 for SQL Server};' + \
               'SERVER={};DATABASE={};UID={};PWD={}'.format(
                   host, database, user, password)

    def _get_metadata_enricher(self):
        return metadata_enricher.MetadataEnricher
