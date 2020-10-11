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

from google.datacatalog_connectors.rdbms.scrape import \
    config_constants, metadata_enricher


class MetadataEnricher(metadata_enricher.MetadataEnricher):

    def enrich(self, scraped_dataframe):
        asset_prefix = self._enrich_metadata_dict.get(
            config_constants.METADATA_ENRICH_ENTRY_PREFIX)

        if asset_prefix:
            table_container_name = self._metadata_definition[
                config_constants.TABLE_CONTAINER_DEF_KEY][
                    config_constants.ASSET_NAME_KEY]
            table_name = self._metadata_definition[
                config_constants.TABLE_DEF_KEY][
                    config_constants.ASSET_NAME_KEY]
            # Update Assets' name with user configured prefix
            scraped_dataframe[
                table_name] = asset_prefix + scraped_dataframe[table_name]
            scraped_dataframe[
                table_container_name] = asset_prefix + scraped_dataframe[
                    table_container_name]

        return scraped_dataframe
