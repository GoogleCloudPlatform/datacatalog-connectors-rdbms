from .config_constants import ROW_COUNT_OPTION


class QueryAssembler:

    def __init__(self):
        pass

    def get_refresh_metadata_queries(self, exact_table_names):
        queries = list()
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
        queries = dict()
        if ROW_COUNT_OPTION in optional_metadata:
            queries[ROW_COUNT_OPTION] = self._get_num_rows_query()
        return queries

    def _get_num_rows_query(self):
        path = self._get_path_to_num_rows_query()
        with open(path, 'r') as f:
            query = f.read()
            return query

    def _get_path_to_num_rows_query(self):
        raise NotImplementedError(
            "Implement to deliver a DB-specific path to the query "
            "for scraping number of rows")
