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

import logging
import warnings
import time

from google.datacatalog_connectors.rdbms.scrape. \
    metadata_sql_objects_normalizer import MetadataSQLObjectsNormalizer

from google.datacatalog_connectors.rdbms.scrape. \
    metadata_scraper import MetadataScraper

import pandas as pd


class MetadataSQLObjectsScraper(MetadataScraper):

    def scrape_sql_objects_metadata(self, user_config, connection_args):
        metadata = None
        if user_config.sql_objects_config:
            query_assembler = self._get_query_assembler()
            sql_objects_config = user_config.sql_objects_config()
            sql_objects_queries = query_assembler.get_sql_objects_queries(
                sql_objects_config)
            logging.info(
                'Scraping metadata according to configuration file: {}'.format(
                    sql_objects_queries))
            metadata = \
                self._get_optional_metadata_from_rdbms_connection(
                    connection_args, sql_objects_queries,
                    metadata_definition)

        return metadata

    def _get_optional_metadata_from_rdbms_connection(self, connection_args,
                                                     optional_queries,
                                                     base_dataframe,
                                                     metadata_definition):
        con = None
        merged_dataframe = base_dataframe
        try:
            con = self._create_rdbms_connection(connection_args)
            cur = con.cursor()
            for option, query in optional_queries.items():
                logging.info(
                    "Executing query to process configuration option {}".
                    format(option))
                cur.execute(query)
                rows = cur.fetchall()
                if len(rows) == 0:
                    warnings.warn(
                        "Query {} delivered no rows. Skipping it.".format(
                            query))
                else:
                    new_dataframe = self._create_dataframe(rows)
                    new_dataframe.columns = [
                        item[0].lower() for item in cur.description
                    ]
                    merged_dataframe = self._get_merged_dataframe(
                        base_dataframe, new_dataframe, metadata_definition)
            return merged_dataframe
        except:  # noqa:E722
            logging.error('Error connecting to the database '
                          'to extract optional metadata.')
            raise
        finally:
            if con:
                con.close()

    def _get_merged_dataframe(self, old_df, new_df, metadata_definition):
        table_name_col = metadata_definition['table_def']['name']
        table_container_mame_col = metadata_definition['table_container_def'][
            'name']
        dataframe = pd.merge(old_df,
                             new_df,
                             on=[table_container_mame_col, table_name_col])
        return dataframe

    # To connect to the RDBMS, it's required to override this method.
    # If you are ingesting from a CSV file, this method is not used.
    def _create_rdbms_connection(self, connection_args):
        raise NotImplementedError(
            'Implementing this method is required to connect to a RDBMS!')

    @classmethod
    def _get_metadata_from_csv(cls, csv_path):
        return pd.read_csv(csv_path)

    def _get_query_assembler(self):
        raise NotImplementedError('Implementing this method is required '
                                  'to run multiple optional queries')
