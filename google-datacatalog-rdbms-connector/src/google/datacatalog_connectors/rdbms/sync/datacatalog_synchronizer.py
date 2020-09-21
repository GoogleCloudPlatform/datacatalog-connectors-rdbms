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
import uuid

from google.datacatalog_connectors.commons.cleanup \
    import datacatalog_metadata_cleaner
from google.datacatalog_connectors.commons.ingest \
    import datacatalog_metadata_ingestor
from google.datacatalog_connectors.commons.monitoring \
    import metrics_processor
from google.datacatalog_connectors.rdbms import prepare


class DataCatalogSynchronizer:
    """Orchestrate the Scrape/Prepare/Ingest steps.

    This Class provides multiple extension points, where
    the RDBMS connector implementation might extend to add
    new fields, Tags, Templates or enrich the metadata information
    (see _get_tag_factory, _get_tag_template_factory, _enrich_metadata
    methods, for some examples, below).

    There are two options to synchronize metadata, from a CSV file
    or a RDBMS connection.

    """

    def __init__(self,
                 project_id,
                 location_id,
                 entry_group_id,
                 rbms_host,
                 metadata_definition,
                 metadata_scraper,
                 connection_args=None,
                 query=None,
                 csv_path=None,
                 enable_monitoring=None,
                 user_config=None):
        self.__entry_group_id = entry_group_id
        self.__metadata_definition = metadata_definition
        self.__metadata_scraper = metadata_scraper
        self.__rbms_host = rbms_host
        self.__project_id = project_id
        self.__location_id = location_id
        self.__connection_args = connection_args
        self.__query = query
        self.__csv_path = csv_path
        self.__user_config = user_config
        self.__task_id = uuid.uuid4().hex[:8]
        self.__metrics_processor = metrics_processor.MetricsProcessor(
            project_id, location_id, entry_group_id, enable_monitoring,
            self.__task_id)

    def run(self):
        """Runs the Scrape, Prepare and Ingest modules
        :return: task_id
        """
        self._before_run()

        logging.info('\n\n==============Scrape metadata===============')

        metadata = self.__metadata_scraper().get_metadata(
            self.__metadata_definition,
            connection_args=self.__connection_args,
            query=self.__query,
            csv_path=self.__csv_path,
            user_config=self.__user_config)

        metadata = self._enrich_metadata(metadata)

        self.__metadata_definition = self._enrich_metadata_definition()

        self._log_metadata(metadata)

        logging.info('\n\n==============Prepare metadata===============')

        tag_templates_dict = self.__create_tag_templates()

        prepared_entries = self.__prepare_datacatalog_entries(
            metadata, tag_templates_dict)

        self._log_entries(prepared_entries)

        logging.info('\n==============Ingest metadata===============')

        self.__delete_obsolete_metadata(prepared_entries)

        self.__ingest_metadata(prepared_entries, tag_templates_dict)

        logging.info('\n============End %s-to-datacatalog============',
                     self.__entry_group_id)
        self._after_run()

        return self.__task_id

    def __prepare_datacatalog_entries(self, metadata, tag_templates_dict):
        entry_factory = self.__create_assembled_entry_factory(
            tag_templates_dict)
        prepared_entries = entry_factory. \
            make_entries_from_table_container_metadata(
                metadata)
        return prepared_entries

    def __delete_obsolete_metadata(self, prepared_entries):
        # Since we can't rely on search returning the ingested entries,
        # we clean up the obsolete entries before ingesting.
        assembled_entries_data = []
        for table_container_entry, table_related_entries in prepared_entries:
            assembled_entries_data.append(table_container_entry)
            assembled_entries_data.extend(table_related_entries)

        cleaner = datacatalog_metadata_cleaner.DataCatalogMetadataCleaner(
            self.__project_id, self.__location_id, self.__entry_group_id)
        cleaner.delete_obsolete_metadata(
            assembled_entries_data, 'system={}'.format(self.__entry_group_id))

    def __ingest_metadata(self, prepared_entries, tag_templates_dict):
        logging.info('\nStarting to ingest custom metadata...')
        ingestor = datacatalog_metadata_ingestor.DataCatalogMetadataIngestor(
            self.__project_id, self.__location_id, self.__entry_group_id)

        for table_container_entry, table_related_entries in prepared_entries:
            assembled_entries_data = []
            assembled_entries_data.append(table_container_entry)
            assembled_entries_data.extend(table_related_entries)
            ingestor.ingest_metadata(assembled_entries_data,
                                     tag_templates_dict)

    def __add_database_name_from_connection_args(self):

        if self.__connection_args:
            database_name = self.__connection_args.get('database')

            if database_name:
                self.__metadata_definition['database_name'] = database_name

    # Create factories
    def __create_assembled_entry_factory(self, tag_templates_dict):
        return self._get_assembled_entry_factory()(
            self.__entry_group_id, self.__metadata_definition,
            self.__create_entry_factory(), self.__create_tag_factory(),
            tag_templates_dict)

    def __create_entry_factory(self):
        return self._get_entry_factory()(self.__project_id, self.__location_id,
                                         self.__rbms_host,
                                         self.__entry_group_id,
                                         self.__metadata_definition)

    def __create_tag_factory(self):
        return self._get_tag_factory()(self.__metadata_definition)

    def __create_tag_templates(self):
        tag_template_factory = self._get_tag_template_factory()(
            self.__project_id, self.__location_id, self.__entry_group_id,
            self.__metadata_definition)

        schema_tag_template_id, schema_tag_template = \
            tag_template_factory. \
            make_tag_template_for_table_container_metadata()

        table_tag_template_id, table_tag_template = \
            tag_template_factory.make_tag_template_for_table_metadata()

        tag_templates_dict = \
            {schema_tag_template_id: schema_tag_template,
             table_tag_template_id: table_tag_template}

        return tag_templates_dict

    # Begin extension methods
    def _before_run(self):
        logging.info('\n============Start %s-to-datacatalog===========',
                     self.__entry_group_id)

    def _after_run(self):
        self.__metrics_processor.process_elapsed_time_metric()

    def _enrich_metadata(self, metadata):
        return metadata

    def _enrich_metadata_definition(self):
        self.__add_database_name_from_connection_args()

        return self.__metadata_definition

    def _log_entries(self, prepared_entries):
        entries_len = sum([len(tables) for (_, tables) in prepared_entries],
                          len(prepared_entries))
        self.__metrics_processor.process_entries_length_metric(entries_len)

    def _log_metadata(self, metadata):
        self.__metrics_processor.process_metadata_payload_bytes_metric(
            metadata)
        logging.info(
            '\n%s table containers ready to be ingested...',
            len(metadata[self.__metadata_definition['table_container_def']
                         ['key']]))

    @classmethod
    def _get_tag_factory(cls):
        return prepare.datacatalog_tag_factory.DataCatalogTagFactory

    @classmethod
    def _get_tag_template_factory(cls):
        return prepare.datacatalog_tag_template_factory. \
            DataCatalogTagTemplateFactory

    @classmethod
    def _get_assembled_entry_factory(cls):
        return prepare.assembled_entry_factory.AssembledEntryFactory

    @classmethod
    def _get_entry_factory(cls):
        return prepare.datacatalog_entry_factory.DataCatalogEntryFactory

    # End extension methods
