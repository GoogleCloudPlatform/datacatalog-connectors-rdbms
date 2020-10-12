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


class MetadataEnricher:

    def __init__(self, metadata_definition, enrich_metadata_dict):
        self._metadata_definition = metadata_definition
        self._enrich_metadata_dict = enrich_metadata_dict

    def enrich(self, scraped_dataframe):
        raise NotImplementedError("Implement this method to enrich "
                                  "attributes of RDBMS assets metadata")
