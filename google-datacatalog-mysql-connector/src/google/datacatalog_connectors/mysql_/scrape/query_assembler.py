# Read configuration file and deliver a list of queries that should be executed to fetch metadata.
# Execute analyze if needed


class QueryAssembler:

    def __init__(self, ingest_config):
        """
        ingest_config: contents of .yaml configuration file
        """
        self._ingest_config = ingest_config

    def _update_metadata(self):
        if self._ingest_config['analyze']:
            self._run_analyze()

    def _run_analyze(self):
        pass

    def _get_base_query(self):
        pass
