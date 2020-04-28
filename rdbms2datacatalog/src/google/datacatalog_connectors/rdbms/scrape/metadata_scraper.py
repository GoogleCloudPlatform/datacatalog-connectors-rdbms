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

from .metadata_normalizer import MetadataNormalizer
import pandas as pd


class MetadataScraper:

    def __init__(self):
        pass

    def get_metadata(self,
                     metadata_definition,
                     connection_args=None,
                     query=None,
                     csv_path=None):
        dataframe = self._get_metadata_as_dataframe(connection_args, query,
                                                    csv_path)

        return MetadataNormalizer.to_metadata_dict(dataframe,
                                                   metadata_definition)

    def _get_metadata_as_dataframe(self,
                                   connection_args=None,
                                   query=None,
                                   csv_path=None):
        if csv_path:
            logging.info('Scrapping metadata from csv path: "%s"', csv_path)
            dataframe = self._get_metadata_from_csv(csv_path)
        elif connection_args and len(connection_args.keys()) > 0:
            logging.info('Scrapping metadata from connection_args')
            dataframe = self._get_metadata_from_rdbms_connection(
                connection_args, query)
        else:
            raise Exception('Must supply either connection_args or csv_path')

        return dataframe

    def _get_metadata_from_rdbms_connection(self, connection_args, query):
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

    # To connect to the RDBMS, it's required to override this method.
    # If you are ingesting from a CSV file, this method is not used.
    def _create_rdbms_connection(self, connection_args):
        raise NotImplementedError(
            'Implementing this method is required to connect to a RDBMS!')

    @classmethod
    def _get_metadata_from_csv(cls, csv_path):
        return pd.read_csv(csv_path)
