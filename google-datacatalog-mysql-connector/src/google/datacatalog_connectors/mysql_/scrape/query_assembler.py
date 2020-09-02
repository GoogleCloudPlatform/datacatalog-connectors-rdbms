# Read configuration file and deliver a list of queries that should be executed to fetch metadata.
# Execute analyze if needed


class QueryAssembler:

    def __init__(self, user_config):
        """
        ingest_config: contents of .yaml configuration file
        """
        self._user_config = user_config

    def get_update_queries(self, table_names):
        queries = list()
        for tbl_name in table_names:
            update_statement = "ANALYZE TABLE {};".format(tbl_name)
            queries.append(update_statement)
        return queries
