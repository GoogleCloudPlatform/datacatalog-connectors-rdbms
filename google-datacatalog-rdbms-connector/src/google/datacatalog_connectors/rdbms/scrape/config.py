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

from google.datacatalog_connectors.rdbms.scrape import config_constants


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
        if self._conf_content.get(config_constants.REFRESH_OPTION) is not None:
            self.refresh_metadata_tables = self._conf_content[
                config_constants.REFRESH_OPTION]
        options = self.get_chosen_metadata_options()

        self.sql_objects_config = self.get_sql_objects_config()

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
            if choice and (option != config_constants.REFRESH_OPTION and
                           option != config_constants.ENRICH_METADATA_OPTION)
        ]
        return options

    def get_sql_objects_config(self):
        parsed_config = []

        sql_objects = self._conf_content.get(config_constants.SQL_OBJECTS_KEY)

        if sql_objects:
            for sql_object in sql_objects:
                if sql_object.get(
                        config_constants.SQL_OBJECT_ITEM_ENABLED_FLAG) is True:
                    item_name = sql_object[
                        config_constants.SQL_OBJECT_ITEM_NAME]
                    parsed_config.append({
                        config_constants.SQL_OBJECT_ITEM_NAME:
                            item_name,
                        config_constants.SQL_OBJECT_ITEM_QUERY_FILENAME_KEY:
                            '{}_{}_{}'.format(
                                config_constants.
                                SQL_OBJECT_ITEM_QUERY_FILENAME_PREFIX,
                                item_name, config_constants.
                                SQL_OBJECT_ITEM_QUERY_FILENAME_SUFFIX),
                        config_constants.SQL_OBJECT_ITEM_METADATA_DEF_FILENAME_KEY:
                            '{}_{}_{}'.format(
                                config_constants.
                                SQL_OBJECT_ITEM_METADATA_DEF_FILENAME_PREFIX,
                                item_name, config_constants.
                                SQL_OBJECT_ITEM_METADATA_DEF_FILENAME_SUFFIX)
                    })

            return parsed_config

    def get_content_dict_attribute(self, attribute_name):
        content_attribute = self._conf_content.get(attribute_name)

        if isinstance(content_attribute, dict):
            return content_attribute

        return None

    def get_enrich_metadata_dict(self):
        return self.get_content_dict_attribute(
            config_constants.ENRICH_METADATA_OPTION)
