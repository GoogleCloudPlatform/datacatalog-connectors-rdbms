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

import pandas as pd

from google.datacatalog_connectors.saphana.scrape import metadata_enricher
from google.datacatalog_connectors.commons_test import utils


class MetadataEnricherTestCase(unittest.TestCase):
    __MODULE_PATH = os.path.dirname(os.path.abspath(__file__))

    def test_enrich_schemas_metadata_with_csv_should_return_objects(self):

        enrich_metadata_dict = {'entry_prefix': 'mycompany'}

        metadata_definition = \
            utils.Utils.convert_json_to_object(
                self.__MODULE_PATH,
                'metadata_definition.json')

        scraped_dataframe = pd.read_csv(
            utils.Utils.get_resolved_file_name(self.__MODULE_PATH,
                                               'saphana_full_dump.csv'))

        enriched_dataframe = metadata_enricher.MetadataEnricher(
            metadata_definition,
            enrich_metadata_dict).enrich(scraped_dataframe)

        self.assertEqual(7, len(enriched_dataframe))
        self.assertTrue(
            enriched_dataframe['schema_name'][0].startswith('mycompany'))
        self.assertTrue(
            enriched_dataframe['table_name'][0].startswith('mycompany'))

    def test_enrich_with_pattern_schemas_metadata_with_csv_should_return_objects(  # noqa: E501
            self):

        enrich_metadata_dict = {
            'entry_prefix': 'mycompany',
            'entry_id_pattern_for_prefix': '^[^a-zA-Z_]+.*$'
        }

        metadata_definition = \
            utils.Utils.convert_json_to_object(
                self.__MODULE_PATH,
                'metadata_definition.json')

        scraped_dataframe = pd.read_csv(
            utils.Utils.get_resolved_file_name(
                self.__MODULE_PATH,
                'sqlserver_full_dump_invalid_asset_names.csv'))

        enriched_dataframe = metadata_enricher.MetadataEnricher(
            metadata_definition,
            enrich_metadata_dict).enrich(scraped_dataframe)

        self.assertEqual(10, len(enriched_dataframe))

        self.assertFalse(
            enriched_dataframe['schema_name'][6].startswith('mycompany'))
        self.assertFalse(
            enriched_dataframe['table_name'][6].startswith('mycompany'))

        self.assertTrue(
            enriched_dataframe['schema_name'][7].startswith('mycompany'))
        self.assertTrue(
            enriched_dataframe['table_name'][7].startswith('mycompany'))

        self.assertFalse(
            enriched_dataframe['schema_name'][8].startswith('mycompany'))
        self.assertFalse(
            enriched_dataframe['table_name'][8].startswith('mycompany'))

        self.assertTrue(
            enriched_dataframe['schema_name'][9].startswith('mycompany'))
        self.assertTrue(
            enriched_dataframe['table_name'][9].startswith('mycompany'))
