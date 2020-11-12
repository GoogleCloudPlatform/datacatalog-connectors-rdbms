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

from google.datacatalog_connectors.saphana.scrape import \
    metadata_enricher, query_assembler


class MetadataScraper(metadata_scraper.MetadataScraper):

    # We use hdbcli over pyhdb since pyhdb is not actively maintained
    # and does not support database arg
    # see: https://stackoverflow.com/questions/63772666/how-to-specifies-database-name-in-pyhdb # noqa
    def _create_rdbms_connection(self, connection_args):
        # import at the method level, because this flow is conditional
        # if the connector reads from a CSV file, this is not used.
        from hdbcli.dbapi import connect

        port = connection_args.get('port')

        if port is None:
            port = 39015

        con = connect(databasename=connection_args['database'],
                      address=connection_args['host'],
                      port=port,
                      user=connection_args['user'],
                      password=connection_args['pass'])
        return con

    def _get_metadata_enricher(self):
        return metadata_enricher.MetadataEnricher

    def _get_query_assembler(self):
        return query_assembler.QueryAssembler()
