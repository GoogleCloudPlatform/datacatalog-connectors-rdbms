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

from .metadata_normalizer import MetadataNormalizer
import pandas as pd


class MetadataScraper:

    def __init__(self):
        pass

    def get_metadata(self,
                     metadata_definition,
                     connection_args=None,
                     query=None,
                     csv_path=None,
                     user_config=None):
        dataframe = self._get_metadata_as_dataframe(metadata_definition,
                                                    connection_args, query,
                                                    csv_path, user_config)

        return MetadataNormalizer.to_metadata_dict(dataframe,
                                                   metadata_definition)

    def _get_metadata_as_dataframe(self,
                                   metadata_definition,
                                   connection_args=None,
                                   query=None,
                                   csv_path=None,
                                   user_config=None):
        if csv_path:
            logging.info('Scrapping metadata from csv path: "%s"', csv_path)
            dataframe = self._get_metadata_from_csv(csv_path)
        elif connection_args and len(connection_args.keys()) > 0:
            logging.info('Scrapping basic metadata from connection_args')
            dataframe = self._get_base_metadata_from_rdbms_connection(
                connection_args, query)
            if user_config:
                query_assembler = self._get_query_assembler(user_config)
                if user_config.update_metadata:
                    tbl_names = MetadataNormalizer.get_table_names_from_dataframe(
                        dataframe, metadata_definition)
                    update_queries = query_assembler.get_update_queries(
                        tbl_names)
                    logging.info('Updating metadata')
                    self._update_metadata_from_rdbms_connection(
                        connection_args, update_queries)
                if user_config.scrape_optional_metadata:
                    optional_metadata = user_config.get_chosen_metadata_options(
                    )
                    optional_queries = query_assembler.get_optional_queries(
                        optional_metadata)
                    logging.info(
                        'Scraping metadata according to configuration file: {}'
                        .format(optional_metadata))
                    column_with_table_names = metadata_definition['table_def'][
                        'name']
                    column_with_container_names = metadata_definition[
                        'table_container_def']['name']
                    dataframe = self._get_optional_metadata_from_rdbms_connection(
                        connection_args, optional_queries, dataframe,
                        column_with_container_names, column_with_table_names)
        else:
            raise Exception('Must supply either connection_args or csv_path')

        return dataframe

    def _get_base_metadata_from_rdbms_connection(self, connection_args, query):
        con = None
        try:
            con = self._create_rdbms_connection(connection_args)
            cur = con.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            dataframe = self._create_dataframe(rows)

            if len(rows) == 0:
                raise Exception('RDBMS is empty, no metadata to extract.')

            dataframe.columns = [item[0].lower() for item in cur.description]
            return dataframe
        except:  # noqa:E722
            logging.error(
                'Error connecting to the database to extract metadata.')
            raise
        finally:
            if con:
                con.close()

    def _create_dataframe(self, rows):
        return pd.DataFrame(rows)

    def _update_metadata_from_rdbms_connection(self, connection_args,
                                               update_queries):
        con = None
        try:
            con = self._create_rdbms_connection(connection_args)
            cur = con.cursor()
            for query in update_queries:
                self._execute_update_query(cur, query)
        except:  # noqa:E722
            logging.error(
                'Error connecting to the database to update metadata.')
            raise
        finally:
            if con:
                con.close()

    def _get_optional_metadata_from_rdbms_connection(self, connection_args,
                                                     optional_queries,
                                                     base_dataframe, cont_name,
                                                     tbl_name):
        con = None
        try:
            con = self._create_rdbms_connection(connection_args)
            cur = con.cursor()
            for query in optional_queries:
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
                    dataframe = pd.merge(base_dataframe,
                                         new_dataframe,
                                         on=[cont_name, tbl_name])
                    base_dataframe = dataframe
            return base_dataframe
        except:  # noqa:E722
            logging.error(
                'Error connecting to the database to extract optional metadata.'
            )
            raise
        finally:
            if con:
                con.close()

    # To connect to the RDBMS, it's required to override this method.
    # If you are ingesting from a CSV file, this method is not used.
    def _create_rdbms_connection(self, connection_args):
        raise NotImplementedError(
            'Implementing this method is required to connect to a RDBMS!')

    @classmethod
    def _get_metadata_from_csv(cls, csv_path):
        return pd.read_csv(csv_path)

    def _get_query_assembler(self, user_config):
        raise NotImplementedError(
            'Implementing this method is required to run multiple optional queries'
        )

    def _execute_update_query(self, cursor, query):
        """
        On update, some DBs deliver a table that has to be fetched after executing the query; others
        don't. What to do with results of update is RDBMS-specific, and these details
         have to be implemented in this method.
        """
        raise NotImplementedError(
            'Implementing this method is required to execute an update query in a DB-specific way'
        )
