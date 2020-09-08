import os
from google.datacatalog_connectors.rdbms.scrape import query_assembler


class QueryAssembler(query_assembler.QueryAssembler):

    def _get_refresh_statement(self, table_name):
        return "ANALYZE {};".format(table_name)

    def _get_path_to_num_rows_query(self):
        return os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'config', 'num_rows_query.sql')
