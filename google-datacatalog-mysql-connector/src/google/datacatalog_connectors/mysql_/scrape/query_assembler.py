from google.datacatalog_connectors.rdbms.scrape import query_assembler


class QueryAssembler(query_assembler.QueryAssembler):

    def _get_update_statement(self, table_name):
        return "ANALYZE TABLE {};".format(table_name)
