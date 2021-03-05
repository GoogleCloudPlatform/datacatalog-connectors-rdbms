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

import os
import unittest

from .. import test_utils
from google.datacatalog_connectors.commons_test import utils
from google.datacatalog_connectors.rdbms.scrape import config
import mock


class MetadataScraperTestCase(unittest.TestCase):
    __MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
    __SCRAPE_PACKAGE = 'google.datacatalog_connectors.rdbms.scrape'
    __NORMALIZER_CLASS = '{}.metadata_normalizer.MetadataNormalizer'.format(
        __SCRAPE_PACKAGE)

    @mock.patch('{}.normalize'.format(__NORMALIZER_CLASS))
    def test_scrape_metadata_with_csv_should_return_objects(self,
                                                            normalize):  # noqa
        metadata = \
            utils.Utils.convert_json_to_object(self.__MODULE_PATH,
                                               'metadata.json')
        normalize.return_value = metadata

        scraper = test_utils.FakeScraper()

        schemas_metadata = scraper.scrape(
            {},
            csv_path=utils.Utils.get_resolved_file_name(
                self.__MODULE_PATH, 'rdbms_full_dump.csv'))

        self.assertEqual(1, len(schemas_metadata))

    @mock.patch('{}.normalize'.format(__NORMALIZER_CLASS))
    def test_scrape_metadata_with_credentials_should_return_objects(
            self, normalize):  # noqa
        metadata = \
            utils.Utils.convert_json_to_object(self.__MODULE_PATH,
                                               'metadata.json')

        normalize.return_value = metadata

        scraper = test_utils.FakeScraper()

        default_query = 'SELECT * from default_db'

        schemas_metadata = scraper.scrape({},
                                          connection_args={
                                              'host': 'localhost',
                                              'port': 1234
                                          },
                                          query=default_query)

        self.assertEqual(default_query, scraper.cur.execute.call_args[0][0])

        self.assertEqual(1, len(schemas_metadata))

    @mock.patch('{}.normalize'.format(__NORMALIZER_CLASS))
    def test_scrape_metadata_with_credentials_overriding_base_metadata_query_should_return_objects(  # noqa: E501
            self, normalize):
        metadata = \
            utils.Utils.convert_json_to_object(self.__MODULE_PATH,
                                               'metadata.json')

        user_config_path = utils.Utils.get_resolved_file_name(
            self.__MODULE_PATH, 'base_metadata_query_ingest_cfg.yaml')
        connector_config_path = utils.Utils.get_test_config_path(
            self.__MODULE_PATH)

        loaded_config = config.Config(user_config_path, connector_config_path)

        normalize.return_value = metadata

        scraper = test_utils.FakeScraper()

        default_query = 'SELECT * from default_db'
        user_defined_override_query = 'SELECT  * from db'

        schemas_metadata = scraper.scrape({},
                                          connection_args={
                                              'host': 'localhost',
                                              'port': 1234
                                          },
                                          query=default_query,
                                          config=loaded_config)

        self.assertEqual(user_defined_override_query,
                         scraper.cur.execute.call_args[0][0])

        self.assertEqual(1, len(schemas_metadata))

    @mock.patch('{}.get_exact_table_names_from_dataframe'.format(
        __NORMALIZER_CLASS,))
    @mock.patch('{}.normalize'.format(__NORMALIZER_CLASS))
    def test_scrape_metadata_with_config_should_return_objects(
            self, normalize, get_exact_table_names_from_dataframe):  # noqa
        metadata = \
            utils.Utils.convert_json_to_object(self.__MODULE_PATH,
                                               'metadata.json')

        normalize.return_value = metadata

        get_exact_table_names_from_dataframe.return_value = [
            "schema0.table0", "schema1.table1"
        ]

        scraper = test_utils.FakeScraper()

        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   '../test_data/ingest_cfg.yaml')

        loaded_config = config.Config(
            config_path, utils.Utils.get_test_config_path(self.__MODULE_PATH))

        metada_def = utils.Utils.get_metadata_def_obj(self.__MODULE_PATH)

        schemas_metadata = scraper.scrape(metada_def,
                                          connection_args={
                                              'host': 'localhost',
                                              'port': 1234
                                          },
                                          config=loaded_config)

        self.assertEqual(1, len(schemas_metadata))

    @mock.patch('{}.get_exact_table_names_from_dataframe'.format(
        __NORMALIZER_CLASS,))
    @mock.patch('{}.normalize'.format(__NORMALIZER_CLASS))
    @mock.patch(
        '{}.sql_objects.sql_objects_metadata_normalizer.'
        'SQLObjectsMetadataNormalizer.normalize'.format(__SCRAPE_PACKAGE))
    def test_scrape_metadata_with_sql_objects_config_should_return_objects(
            self, sql_objects_normalize, base_normalize,
            get_exact_table_names_from_dataframe):  # noqa
        base_metadata = \
            utils.Utils.convert_json_to_object(self.__MODULE_PATH,
                                               'metadata.json')

        base_normalize.return_value = base_metadata

        functions_metadata = \
            utils.Utils.convert_json_to_object(self.__MODULE_PATH,
                                               'normalized_sql_objects.json')

        sql_objects_normalize.return_value = functions_metadata

        get_exact_table_names_from_dataframe.return_value = [
            "schema0.table0", "schema1.table1"
        ]

        scraper = test_utils.FakeScraper()

        user_config_path = utils.Utils.get_resolved_file_name(
            self.__MODULE_PATH, 'sql_objects_ingest_cfg.yaml')
        connector_config_path = utils.Utils.get_test_config_path(
            self.__MODULE_PATH)

        loaded_config = config.Config(user_config_path, connector_config_path)

        metada_def = utils.Utils.get_metadata_def_obj(self.__MODULE_PATH)

        scraped_metadata = scraper.scrape(metada_def,
                                          connection_args={
                                              'host': 'localhost',
                                              'port': 1234
                                          },
                                          config=loaded_config)

        self.assertEqual(2, len(scraped_metadata))
        self.assertIn('schemas', scraped_metadata)
        self.assertIn('sql_objects', scraped_metadata)
        self.assertDictEqual(base_metadata, scraped_metadata)
        self.assertDictEqual(functions_metadata,
                             scraped_metadata['sql_objects']['functions'])

    @mock.patch('{}.get_exact_table_names_from_dataframe'.format(
        __NORMALIZER_CLASS,))
    @mock.patch('{}.normalize'.format(__NORMALIZER_CLASS))
    @mock.patch(
        '{}.sql_objects.sql_objects_metadata_normalizer.'
        'SQLObjectsMetadataNormalizer.normalize'.format(__SCRAPE_PACKAGE))
    def test_scrape_metadata_with_multiple_sql_objects_config_should_return_objects(  # noqa: E501
            self, sql_objects_normalize, base_normalize,
            get_exact_table_names_from_dataframe):  # noqa
        base_metadata = \
            utils.Utils.convert_json_to_object(self.__MODULE_PATH,
                                               'metadata.json')

        base_normalize.return_value = base_metadata

        functions_metadata = \
            utils.Utils.convert_json_to_object(self.__MODULE_PATH,
                                               'normalized_sql_objects.json')

        stored_procedure_metadata = \
            utils.Utils.convert_json_to_object(
                self.__MODULE_PATH,
                'normalized_sql_objects_stored_procedure.json')

        sql_objects_normalize.side_effect = [
            functions_metadata, stored_procedure_metadata
        ]

        get_exact_table_names_from_dataframe.return_value = [
            "schema0.table0", "schema1.table1"
        ]

        scraper = test_utils.FakeScraper()

        user_config_path = utils.Utils.get_resolved_file_name(
            self.__MODULE_PATH, 'sql_objects_ingest_cfg.yaml')
        connector_config_path = utils.Utils.get_test_config_path(
            self.__MODULE_PATH)

        loaded_config = config.Config(user_config_path, connector_config_path)

        metada_def = utils.Utils.get_metadata_def_obj(self.__MODULE_PATH)

        scraped_metadata = scraper.scrape(metada_def,
                                          connection_args={
                                              'host': 'localhost',
                                              'port': 1234
                                          },
                                          config=loaded_config)

        self.assertEqual(2, len(scraped_metadata))
        self.assertIn('schemas', scraped_metadata)
        self.assertIn('sql_objects', scraped_metadata)
        self.assertDictEqual(base_metadata, scraped_metadata)
        self.assertDictEqual(functions_metadata,
                             scraped_metadata['sql_objects']['functions'])
        self.assertDictEqual(
            stored_procedure_metadata,
            scraped_metadata['sql_objects']['stored_procedures'])

    @mock.patch('{}.get_exact_table_names_from_dataframe'.format(
        __NORMALIZER_CLASS,))
    @mock.patch('{}.normalize'.format(__NORMALIZER_CLASS))
    def test_scrape_metadata_with_enrich_metadata_config_should_return_objects(  # noqa:E501
            self, normalize, get_exact_table_names_from_dataframe):  # noqa
        metadata = \
            utils.Utils.convert_json_to_object(self.__MODULE_PATH,
                                               'metadata.json')

        normalize.return_value = metadata

        get_exact_table_names_from_dataframe.return_value = [
            "schema0.table0", "schema1.table1"
        ]

        scraper = test_utils.FakeScraperWithMetadataEnricher()

        config_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '../test_data/enrich_metadata_ingest_cfg.yaml')

        loaded_config = config.Config(
            config_path, utils.Utils.get_test_config_path(self.__MODULE_PATH))

        metada_def = utils.Utils.get_metadata_def_obj(self.__MODULE_PATH)

        schemas_metadata = scraper.scrape(metada_def,
                                          connection_args={
                                              'host': 'localhost',
                                              'port': 1234
                                          },
                                          config=loaded_config)

        self.assertEqual(1, len(schemas_metadata))

        metadata_dataframe, metadata_definition = \
            normalize.call_args_list[0][0]
        self.assertTrue(
            metadata_dataframe['schema_name'][0].startswith('mycompany'))
        self.assertTrue(
            metadata_dataframe['table_name'][0].startswith('mycompany'))

    @mock.patch('{}.get_exact_table_names_from_dataframe'.format(
        __NORMALIZER_CLASS,))
    @mock.patch('{}.normalize'.format(__NORMALIZER_CLASS))
    def test_scrape_metadata_with_csv_and_config_should_return_objects(
            self, normalize, get_exact_table_names_from_dataframe):  # noqa

        metadata = \
            utils.Utils.convert_json_to_object(self.__MODULE_PATH,
                                               'metadata.json')
        normalize.return_value = metadata

        get_exact_table_names_from_dataframe.return_value = [
            "schema0.table0", "schema1.table1"
        ]

        scraper = test_utils.FakeScraperWithMetadataEnricher()

        config_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '../test_data/enrich_metadata_ingest_cfg.yaml')

        loaded_config = config.Config(
            config_path, utils.Utils.get_test_config_path(self.__MODULE_PATH))

        metada_def = utils.Utils.get_metadata_def_obj(self.__MODULE_PATH)

        schemas_metadata = scraper.scrape(
            metada_def,
            csv_path=utils.Utils.get_resolved_file_name(
                self.__MODULE_PATH, 'rdbms_full_dump.csv'),
            config=loaded_config)

        self.assertEqual(1, len(schemas_metadata))

        metadata_dataframe, metadata_definition = \
            normalize.call_args_list[0][0]
        self.assertTrue(
            metadata_dataframe['schema_name'][0].startswith('mycompany'))
        self.assertTrue(
            metadata_dataframe['table_name'][0].startswith('mycompany'))

    @mock.patch('{}.get_exact_table_names_from_dataframe'.format(
        __NORMALIZER_CLASS,))
    @mock.patch('{}.normalize'.format(__NORMALIZER_CLASS))
    @mock.patch(
        '{}.sql_objects.sql_objects_metadata_normalizer.'
        'SQLObjectsMetadataNormalizer.normalize'.format(__SCRAPE_PACKAGE))
    def test_scrape_metadata_with_csv_and_sql_objects_should_return_base_metadata(  # noqa: E501
            self, sql_objects_normalize, base_normalize,
            get_exact_table_names_from_dataframe):  # noqa
        base_metadata = \
            utils.Utils.convert_json_to_object(self.__MODULE_PATH,
                                               'metadata.json')

        base_normalize.return_value = base_metadata

        functions_metadata = \
            utils.Utils.convert_json_to_object(self.__MODULE_PATH,
                                               'normalized_sql_objects.json')

        sql_objects_normalize.return_value = functions_metadata

        get_exact_table_names_from_dataframe.return_value = [
            "schema0.table0", "schema1.table1"
        ]

        scraper = test_utils.FakeScraper()

        user_config_path = utils.Utils.get_resolved_file_name(
            self.__MODULE_PATH, 'sql_objects_ingest_cfg.yaml')
        connector_config_path = utils.Utils.get_test_config_path(
            self.__MODULE_PATH)

        loaded_config = config.Config(user_config_path, connector_config_path)

        metada_def = utils.Utils.get_metadata_def_obj(self.__MODULE_PATH)

        scraped_metadata = scraper.scrape(
            metada_def,
            csv_path=utils.Utils.get_resolved_file_name(
                self.__MODULE_PATH, 'rdbms_full_dump.csv'),
            config=loaded_config)

        self.assertEqual(1, len(scraped_metadata))
        self.assertIn('schemas', scraped_metadata)
        self.assertNotIn('sql_objects', scraped_metadata)
        self.assertDictEqual(base_metadata, scraped_metadata)

    @mock.patch('{}.get_exact_table_names_from_dataframe'.format(
        __NORMALIZER_CLASS,))
    @mock.patch('{}.normalize'.format(__NORMALIZER_CLASS))
    def test_scrape_metadata_with_enrich_metadata_config_and_no_enricher_should_succeed(  # noqa:E501
            self, normalize, _):  # noqa
        metadata = \
            utils.Utils.convert_json_to_object(self.__MODULE_PATH,
                                               'metadata.json')

        normalize.return_value = metadata

        config_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '../test_data/enrich_metadata_ingest_cfg.yaml')

        loaded_config = config.Config(
            config_path, utils.Utils.get_test_config_path(self.__MODULE_PATH))

        metada_def = utils.Utils.get_metadata_def_obj(self.__MODULE_PATH)

        scraper = test_utils.FakeScraper()

        scraper.scrape(metada_def,
                       connection_args={
                           'host': 'localhost',
                           'port': 1234
                       },
                       config=loaded_config)

    @mock.patch('{}.normalize'.format(__NORMALIZER_CLASS))
    def test_scrape_metadata_on_exception_should_re_raise(self,
                                                          normalize):  # noqa
        scraper = test_utils.FakeScraper()

        self.assertRaises(Exception, scraper.scrape, {})

        self.assertEqual(normalize.call_count, 0)

    @mock.patch('{}.normalize'.format(__NORMALIZER_CLASS))
    def test_scrape_metadata_on_connection_exception_should_re_raise(
            self, normalize):  # noqa
        scraper = test_utils.FakeScraperWithConError()

        self.assertRaises(Exception,
                          scraper.scrape, {},
                          connection_args={
                              'host': 'localhost',
                              'port': 1234
                          })

        self.assertEqual(normalize.call_count, 0)

    @mock.patch('{}.normalize'.format(__NORMALIZER_CLASS))
    @mock.patch('{}.query_assembler.QueryAssembler.'
                'get_refresh_metadata_queries'.format(__SCRAPE_PACKAGE))
    def test_metadata_should_not_be_updated_without_config(
            self, get_refresh_metadata_queries, normalize):
        scraper = test_utils.FakeScraper()
        metadata = \
            utils.Utils.convert_json_to_object(self.__MODULE_PATH,
                                               'metadata.json')

        normalize.return_value = metadata
        schemas_metadata = scraper.scrape({},
                                          connection_args={
                                              'host': 'localhost',
                                              'port': 1234
                                          },
                                          config=None)

        self.assertEqual(1, len(schemas_metadata))
        self.assertEqual(0, get_refresh_metadata_queries.call_count)

    @mock.patch('{}.normalize'.format(__NORMALIZER_CLASS))
    @mock.patch(
        '{}.query_assembler.QueryAssembler.get_optional_queries'.format(
            __SCRAPE_PACKAGE))
    def test_optional_metadata_should_not_be_pulled_without_config(
            self, get_optional_queries, normalize):
        scraper = test_utils.FakeScraper()
        metadata = \
            utils.Utils.convert_json_to_object(self.__MODULE_PATH,
                                               'metadata.json')

        normalize.return_value = metadata
        schemas_metadata = scraper.scrape({},
                                          connection_args={
                                              'host': 'localhost',
                                              'port': 1234
                                          },
                                          config=None)

        self.assertEqual(1, len(schemas_metadata))
        self.assertEqual(0, get_optional_queries.call_count)

    @mock.patch('{}.normalize'.format(__NORMALIZER_CLASS))
    @mock.patch('{}.query_assembler.QueryAssembler.'
                'get_refresh_metadata_queries'.format(__SCRAPE_PACKAGE))
    def test_metadata_should_not_be_updated_with_empty_config(
            self, get_refresh_metadata_queries, normalize):
        path_to_empty_config = utils.Utils.get_resolved_file_name(
            self.__MODULE_PATH, 'empty_ingest_cfg.yaml')
        empty_config = config.Config(
            path_to_empty_config,
            utils.Utils.get_test_config_path(self.__MODULE_PATH))

        scraper = test_utils.FakeScraper()
        metadata = \
            utils.Utils.convert_json_to_object(self.__MODULE_PATH,
                                               'metadata.json')

        normalize.return_value = metadata
        schemas_metadata = scraper.scrape({},
                                          connection_args={
                                              'host': 'localhost',
                                              'port': 1234
                                          },
                                          config=empty_config)
        self.assertEqual(1, len(schemas_metadata))
        self.assertEqual(0, get_refresh_metadata_queries.call_count)

    @mock.patch('{}.normalize'.format(__NORMALIZER_CLASS))
    @mock.patch(
        '{}.query_assembler.QueryAssembler.get_optional_queries'.format(
            __SCRAPE_PACKAGE))
    def test_optional_metadata_should_not_be_pulled_with_empty_config(
            self, get_optional_queries, normalize):
        path_to_empty_config = utils.Utils.get_resolved_file_name(
            self.__MODULE_PATH, 'empty_ingest_cfg.yaml')
        empty_config = config.Config(
            path_to_empty_config,
            utils.Utils.get_test_config_path(self.__MODULE_PATH))

        scraper = test_utils.FakeScraper()
        metadata = \
            utils.Utils.convert_json_to_object(self.__MODULE_PATH,
                                               'metadata.json')

        normalize.return_value = metadata
        schemas_metadata = scraper.scrape({},
                                          connection_args={
                                              'host': 'localhost',
                                              'port': 1234
                                          },
                                          config=empty_config)
        self.assertEqual(1, len(schemas_metadata))
        self.assertEqual(0, get_optional_queries.call_count)
