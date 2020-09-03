import os
from google.datacatalog_connectors.rdbms.scrape import query_assembler


class QueryAssembler(query_assembler.QueryAssembler):

    def _get_update_statement(self, table_name):
        return "ANALYZE TABLE {};".format(table_name)

    def get_optional_queries(self, optional_metadata):
        queries = list()
        if 'num_rows' in optional_metadata:
            queries.append(self._get_num_rows_query())
        return queries

    def _get_num_rows_query(self):
        path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'config', 'num_rows_query.sql')
        with open(path, 'r') as f:
            query = f.read()
            return query
