import os
from google.datacatalog_connectors.rdbms.scrape import query_assembler


class QueryAssembler(query_assembler.QueryAssembler):

    def _get_update_statement(self, schema_table_pair):
        exact_table_name = ".".join(schema_table_pair)
        return "ANALYZE {};".format(exact_table_name)

    def _get_path_to_num_rows_query(self):
        return os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'config', 'num_rows_query.sql')
