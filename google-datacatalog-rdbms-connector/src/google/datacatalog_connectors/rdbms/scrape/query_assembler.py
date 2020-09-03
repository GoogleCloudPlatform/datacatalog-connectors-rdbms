class QueryAssembler:

    def __init__(self):
        pass

    def get_update_queries(self, table_names):
        queries = list()
        for tbl_name in table_names:
            update_statement = self._get_update_statement(tbl_name)
            queries.append(update_statement)
        return queries

    def _get_update_statement(self, tbl_name):
        raise NotImplementedError(
            "Implement this method to get a DB-specific update method")

    def get_optional_queries(self, optional_metadata):
        queries = list()
        if 'num_rows' in optional_metadata:
            queries.append(self._get_num_rows_query())
        return queries

    def _get_num_rows_query(self):
        path = self._get_path_to_num_rows_query()
        with open(path, 'r') as f:
            query = f.read()
            return query

    def _get_path_to_num_rows_query(self):
        raise NotImplementedError(
            "Implement to deliver a DB-specific path to the num_rows query")
