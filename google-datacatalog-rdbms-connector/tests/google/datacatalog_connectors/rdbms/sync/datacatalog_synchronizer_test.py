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

import mock
import os
import unittest

from .. import test_utils
from google.datacatalog_connectors.commons_test import utils
from google.datacatalog_connectors.rdbms.sync import \
    datacatalog_synchronizer
from google.datacatalog_connectors.rdbms.scrape import \
    config


@mock.patch('google.datacatalog_connectors.rdbms.scrape.metadata_scraper.'
            'MetadataScraper.'
            '__init__', lambda self, *args: None)
@mock.patch('google.datacatalog_connectors.rdbms.prepare.'
            'assembled_entry_factory.AssembledEntryFactory.__init__',
            lambda self, *args: None)
@mock.patch(
    'google.datacatalog_connectors.commons.ingest.'
    'datacatalog_metadata_ingestor.DataCatalogMetadataIngestor.__init__',
    lambda self, *args: None)
@mock.patch('google.datacatalog_connectors.commons.cleanup.'
            'datacatalog_metadata_cleaner.DataCatalogMetadataCleaner.__init__',
            lambda self, *args: None)
@mock.patch('google.datacatalog_connectors.commons.monitoring.'
            'metrics_processor.MetricsProcessor.__init__',
            lambda self, *args: None)
class DatacatalogSynchronizerTestCase(unittest.TestCase):
    __MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
    __RDBMS_PACKAGE = 'google.datacatalog_connectors.rdbms'
    __COMMONS_PACKAGE = 'google.datacatalog_connectors.commons'
    __PROJECT_ID = 'test_project'
    __LOCATION_ID = 'location_id'
    __HOST = 'localhost'
    __ENTRY_GROUP_ID = 'rdbms'
    __RAW_METADATA_CSV = 'csv'

    @mock.patch('google.datacatalog_connectors.rdbms.'
                'scrape.metadata_scraper.MetadataScraper.scrape')
    @mock.patch('google.datacatalog_connectors.rdbms.'
                'prepare.sql_objects.assembled_sql_objects_entry_factory.'
                'AssembledSQLObjectsEntryFactory.make_entries')
    @mock.patch('google.datacatalog_connectors.rdbms.'
                'prepare.assembled_entry_factory.'
                'AssembledEntryFactory.make_entries')
    @mock.patch('google.datacatalog_connectors.commons.ingest.'
                'datacatalog_metadata_ingestor.'
                'DataCatalogMetadataIngestor.ingest_metadata')
    @mock.patch('google.datacatalog_connectors.commons.cleanup.'
                'datacatalog_metadata_cleaner.DataCatalogMetadataCleaner.'
                'delete_obsolete_metadata')
    @mock.patch('google.datacatalog_connectors.commons.monitoring.'
                'metrics_processor.MetricsProcessor.'
                'process_elapsed_time_metric')
    @mock.patch('google.datacatalog_connectors.commons.monitoring.'
                'metrics_processor.MetricsProcessor.'
                'process_metadata_payload_bytes_metric')
    @mock.patch('google.datacatalog_connectors.commons.monitoring.'
                'metrics_processor.MetricsProcessor.'
                'process_entries_length_metric')
    def test_synchronize_metadata_should_not_raise_error(  # noqa: E125
            self, process_entries_length_metric,
            process_metadata_payload_bytes_metric, process_elapsed_time_metric,
            delete_obsolete_metadata, ingest_metadata, make_base_entries,
            make_sql_objects_entries, scrape):
        make_base_entries.return_value = [({}, [])]
        make_sql_objects_entries.return_value = []

        synchronizer = datacatalog_synchronizer.DataCatalogSynchronizer(
            DatacatalogSynchronizerTestCase.__PROJECT_ID,
            DatacatalogSynchronizerTestCase.__LOCATION_ID,
            DatacatalogSynchronizerTestCase.__ENTRY_GROUP_ID,
            DatacatalogSynchronizerTestCase.__HOST,
            utils.Utils.get_metadata_def_obj(self.__MODULE_PATH),
            test_utils.FakeScraper, {'database': 'test_db'},
            enable_monitoring=True)

        synchronizer.run()
        self.assertEqual(scrape.call_count, 1)
        self.assertEqual(
            synchronizer.
            _DataCatalogSynchronizer__metadata_definition['database_name'],
            'test_db')
        self.assertEqual(make_base_entries.call_count, 1)
        self.assertEqual(ingest_metadata.call_count, 1)
        self.assertEqual(delete_obsolete_metadata.call_count, 1)
        self.assertEqual(process_entries_length_metric.call_count, 1)
        self.assertEqual(process_metadata_payload_bytes_metric.call_count, 1)
        self.assertEqual(process_elapsed_time_metric.call_count, 1)

    @mock.patch('google.datacatalog_connectors.rdbms.'
                'scrape.metadata_scraper.MetadataScraper.scrape')
    @mock.patch('google.datacatalog_connectors.rdbms.'
                'prepare.sql_objects.assembled_sql_objects_entry_factory.'
                'AssembledSQLObjectsEntryFactory.make_entries')
    @mock.patch('google.datacatalog_connectors.rdbms.'
                'prepare.assembled_entry_factory.'
                'AssembledEntryFactory.make_entries')
    @mock.patch('google.datacatalog_connectors.commons.ingest.'
                'datacatalog_metadata_ingestor.'
                'DataCatalogMetadataIngestor.ingest_metadata')
    @mock.patch('google.datacatalog_connectors.commons.cleanup.'
                'datacatalog_metadata_cleaner.DataCatalogMetadataCleaner.'
                'delete_obsolete_metadata')
    @mock.patch('google.datacatalog_connectors.commons.monitoring.'
                'metrics_processor.MetricsProcessor.'
                'process_elapsed_time_metric')
    @mock.patch('google.datacatalog_connectors.commons.monitoring.'
                'metrics_processor.MetricsProcessor.'
                'process_metadata_payload_bytes_metric')
    @mock.patch('google.datacatalog_connectors.commons.monitoring.'
                'metrics_processor.MetricsProcessor.'
                'process_entries_length_metric')
    def test_synchronize_metadata_with_sql_config_should_not_raise_error(  # noqa: E501
            self, process_entries_length_metric,
            process_metadata_payload_bytes_metric, process_elapsed_time_metric,
            delete_obsolete_metadata, ingest_metadata, make_base_entries,
            make_sql_objects_entries, scrape):
        make_base_entries.return_value = [({}, [])]
        make_sql_objects_entries.return_value = []

        user_config_path = utils.Utils.get_resolved_file_name(
            self.__MODULE_PATH, 'sql_objects_ingest_cfg.yaml')
        connector_config_path = utils.Utils.get_test_config_path(
            self.__MODULE_PATH)

        loaded_config = config.Config(user_config_path, connector_config_path)

        synchronizer = datacatalog_synchronizer.DataCatalogSynchronizer(
            DatacatalogSynchronizerTestCase.__PROJECT_ID,
            DatacatalogSynchronizerTestCase.__LOCATION_ID,
            DatacatalogSynchronizerTestCase.__ENTRY_GROUP_ID,
            DatacatalogSynchronizerTestCase.__HOST,
            utils.Utils.get_metadata_def_obj(self.__MODULE_PATH),
            test_utils.FakeScraper, {'database': 'test_db'},
            enable_monitoring=True,
            config=loaded_config)

        synchronizer.run()
        self.assertEqual(scrape.call_count, 1)
        self.assertEqual(
            synchronizer.
            _DataCatalogSynchronizer__metadata_definition['database_name'],
            'test_db')
        self.assertEqual(make_base_entries.call_count, 1)
        self.assertEqual(ingest_metadata.call_count, 2)
        self.assertEqual(delete_obsolete_metadata.call_count, 1)
        self.assertEqual(process_entries_length_metric.call_count, 1)
        self.assertEqual(process_metadata_payload_bytes_metric.call_count, 1)
        self.assertEqual(process_elapsed_time_metric.call_count, 1)
