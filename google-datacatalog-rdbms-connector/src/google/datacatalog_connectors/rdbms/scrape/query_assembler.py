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

from google.datacatalog_connectors.rdbms.common import constants


class QueryAssembler:

    def __init__(self):
        pass

    def get_refresh_metadata_queries(self, exact_table_names):
        queries = []
        for name in exact_table_names:
            refresh_statement = self._get_refresh_statement(name)
            queries.append(refresh_statement)
        return queries

    def _get_refresh_statement(self, tbl_name):
        raise NotImplementedError(
            "Implement this method to get a DB-specific update method")

    def get_optional_queries(self, optional_metadata):
        """
        Extend this method to add more optional queries
        """
        queries = {}
        if constants.ROW_COUNT_OPTION in optional_metadata:
            queries[constants.ROW_COUNT_OPTION] = self._get_num_rows_query()
        return queries

    def _get_num_rows_query(self):
        return self._get_query(self._get_path_to_num_rows_query())

    def _get_path_to_num_rows_query(self):
        raise NotImplementedError(
            "Implement to deliver a DB-specific path to the query "
            "for scraping number of rows")

    def _get_connector_query_dir_path(self):
        raise NotImplementedError(
            "Implement to specify the query dir used by the connector")

    @classmethod
    def _get_query(cls, query_path):
        with open(query_path, 'r') as f:
            query = f.read()
            return query
