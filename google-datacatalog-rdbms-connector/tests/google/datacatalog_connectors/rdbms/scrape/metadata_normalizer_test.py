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

from google.datacatalog_connectors.commons_test import utils
from google.datacatalog_connectors.rdbms.scrape \
    import metadata_normalizer


class MetadataNormalizerTestCase(unittest.TestCase):
    __MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
    __SCRAPE_PACKAGE = 'google.datacatalog_connectors.rdbms.scrape'

    def test_normalize_databases_metadata_with_csv_should_return_objects(self):
        metadata = utils.Utils.retrieve_dataframe_from_file(
            self.__MODULE_PATH, 'rdbms_full_dump.csv')

        expected_metadata = utils.Utils.convert_json_to_object(
            self.__MODULE_PATH, 'metadata.json')

        metadata_dict = \
            metadata_normalizer.MetadataNormalizer. \
            to_metadata_dict(
                metadata,
                utils.Utils.get_metadata_def_obj(self.__MODULE_PATH))

        # Convert the metadata objects to string so we
        # can compare all json fields, and guarantee that they are equal.
        self.assertEqual(utils.Utils.convert_json_to_str(expected_metadata),
                         utils.Utils.convert_json_to_str(metadata_dict))

    def test_normalizer_should_build_exact_table_names(self):
        test_rows = [[" Schema1", "Table1"], ["Schema1", " Table2"],
                     ["Schema1", "Table3"], ["Schema2  ", "Table1"],
                     ["Schema2", "Table4"], ["Schema2", "Table5"]]
        metadata_def = utils.Utils.get_metadata_def_obj(self.__MODULE_PATH)
        columns_names = [
            metadata_def["table_container_def"]["name"],
            metadata_def["table_def"]["name"]
        ]
        test_df = pd.DataFrame(test_rows, columns=columns_names)
        exact_table_names = metadata_normalizer.MetadataNormalizer.\
            get_exact_table_names_from_dataframe(
                test_df, metadata_def)
        expected_table_names = [
            "Schema1.Table1", "Schema1.Table2", "Schema1.Table3",
            "Schema2.Table1", "Schema2.Table4", "Schema2.Table5"
        ]
        self.assertCountEqual(expected_table_names, exact_table_names)
