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

import yaml

from .config_constants import ENRICH_METADATA_OPTION
from .config_constants import REFRESH_OPTION


class Config:

    def __init__(self, config_path):
        self._config_path = config_path
        self._conf_content = self._read_config_file()
        self.refresh_metadata_tables = False
        self.scrape_optional_metadata = False
        self._determine_scraping_steps()

    def _read_config_file(self):
        with open(self._config_path, 'r') as f:
            conf = yaml.load(f, Loader=yaml.FullLoader)
        return conf or dict()

    def _determine_scraping_steps(self):
        if self._conf_content.get(REFRESH_OPTION) is not None:
            self.refresh_metadata_tables = self._conf_content[REFRESH_OPTION]
        options = self.get_chosen_metadata_options()

        if len(options):
            self.scrape_optional_metadata = True

    def get_chosen_metadata_options(self):
        '''
        From the config contents, retrieve options that user has marked as true
        '''
        options = [
            # TODO put the scrape_options in a parent
            #  key in the user def config
            option
            for option, choice in self._conf_content.items()
            if choice and
            (option != REFRESH_OPTION and option != ENRICH_METADATA_OPTION)
        ]
        return options

    def get_content_dict_attribute(self, attribute_name):
        content_attribute = self._conf_content.get(attribute_name)

        if isinstance(content_attribute, dict):
            return content_attribute

        return None

    def get_enrich_metadata_dict(self):
        return self.get_content_dict_attribute(ENRICH_METADATA_OPTION)
