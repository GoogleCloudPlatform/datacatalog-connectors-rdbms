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

import re

from google.datacatalog_connectors.rdbms.common import constants
from google.datacatalog_connectors.rdbms.scrape import \
    metadata_enricher


class BaseMetadataEnricher(metadata_enricher.MetadataEnricher):

    def enrich(self, scraped_dataframe):
        asset_prefix = self._enrich_metadata_dict.get(
            constants.METADATA_ENRICH_ENTRY_PREFIX)

        if asset_prefix:
            table_container_name = self._metadata_definition[
                constants.TABLE_CONTAINER_DEF_KEY][constants.ASSET_NAME_KEY]
            table_name = self._metadata_definition[constants.TABLE_DEF_KEY][
                constants.ASSET_NAME_KEY]

            column_name = self._metadata_definition[constants.COLUMN_DEF_KEY][
                constants.ASSET_NAME_KEY]

            asset_pattern_for_prefix = self._enrich_metadata_dict.get(
                constants.METADATA_ENRICH_ENTRY_ID_PATTERN_FOR_PREFIX)

            scraped_dataframe[table_name] = \
                scraped_dataframe[table_name].apply(
                    self.__apply_prefix,
                    args=(asset_prefix,
                          asset_pattern_for_prefix))

            scraped_dataframe[column_name] = \
                scraped_dataframe[column_name].apply(
                    self.__apply_prefix,
                    args=(asset_prefix,
                          asset_pattern_for_prefix))

            scraped_dataframe[table_container_name] = \
                scraped_dataframe[table_container_name].apply(
                    self.__apply_prefix,
                    args=(asset_prefix,
                          asset_pattern_for_prefix))

        return scraped_dataframe

    # Update Assets' name with user configured prefix
    @classmethod
    def __apply_prefix(cls, val, asset_prefix, asset_pattern_for_prefix):
        if asset_pattern_for_prefix:
            match = re.match(pattern=asset_pattern_for_prefix, string=val)
            if match:
                return asset_prefix + val
            else:
                return val

        else:
            return asset_prefix + val
