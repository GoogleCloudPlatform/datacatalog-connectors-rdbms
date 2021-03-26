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
import json
import os

from google.datacatalog_connectors.commons import config
from google.datacatalog_connectors.rdbms.common import constants


class Config:

    def __init__(self, user_config_path, connector_config_path):
        self._user_config_path = user_config_path
        self._connector_config_path = connector_config_path
        self._conf_content = self.__read_yaml_file(self._user_config_path)
        self.refresh_metadata_tables = False
        self.scrape_optional_metadata = False
        self.__determine_scraping_steps()

    def get_chosen_metadata_options(self):
        """
        Retrieve options the user has marked as true from the config contents.
        """
        options = [
            # TODO put the scrape_options in a parent
            #  key in the user def config
            option
            for option, choice in self._conf_content.items()
            if choice and (option != constants.REFRESH_OPTION and
                           option != constants.ENRICH_METADATA_OPTION and
                           option != constants.BASE_METADATA_QUERY_FILENAME and
                           option != constants.SQL_OBJECTS_KEY)
        ]
        return options

    def get_enrich_metadata_dict(self):
        return self.__get_content_dict_attribute(
            constants.ENRICH_METADATA_OPTION)

    def __get_base_metadata_query_config(self):
        base_metadata_query_filename = self._conf_content.get(
            constants.BASE_METADATA_QUERY_FILENAME)

        if not base_metadata_query_filename:
            return

        query_full_path = os.path.join(self._connector_config_path,
                                       base_metadata_query_filename)

        if self.__file_exists(query_full_path):
            logging.info('Loading the override base metadata query at: %s',
                         query_full_path)
            return self.__read_sql_query_file(query_full_path)

    def __get_sql_objects_config(self):
        parsed_config = {}

        sql_objects = self._conf_content.get(constants.SQL_OBJECTS_KEY)

        if not sql_objects:
            return parsed_config

        for sql_object in sql_objects:
            if not sql_object.get(constants.SQL_OBJECT_ITEM_ENABLED_FLAG):
                continue

            # Check to avoid breaking changes,
            # older versions of connector will skip this.
            if self._connector_config_path:
                item_name = sql_object[constants.SQL_OBJECT_ITEM_NAME]

                query_path = '{}_{}_{}'.format(
                    constants.SQL_OBJECT_ITEM_QUERY_FILENAME_PREFIX, item_name,
                    constants.SQL_OBJECT_ITEM_QUERY_FILENAME_SUFFIX)

                query_full_path = os.path.join(self._connector_config_path,
                                               query_path)

                metadata_def_path = '{}_{}_{}'.format(
                    constants.SQL_OBJECT_ITEM_METADATA_DEF_FILENAME_PREFIX,
                    item_name,
                    constants.SQL_OBJECT_ITEM_METADATA_DEF_FILENAME_SUFFIX)

                metadata_def_full_path = os.path.join(
                    self._connector_config_path, metadata_def_path)

                if self.__connector_has_config_files_for_sql_objects(
                        query_full_path, metadata_def_full_path):

                    sql_object_item_key =\
                        constants.SQL_OBJECT_ITEM_NAME

                    sql_object_query_key =\
                        constants.SQL_OBJECT_ITEM_QUERY_KEY

                    sql_object_metadata_def_key =\
                        constants.\
                        SQL_OBJECT_ITEM_METADATA_DEF_KEY

                    query_value = self.\
                        __read_sql_query_file(query_full_path)

                    parsed_config[item_name] = {
                        sql_object_item_key:
                            item_name,
                        sql_object_query_key:
                            query_value,
                        sql_object_metadata_def_key:
                            self.__read_json_file(metadata_def_full_path)
                    }

                    logging.info(
                        'SQL Object: %s processed, metadata def: %s'
                        ' and query: %s', item_name, metadata_def_full_path,
                        query_full_path)
                else:
                    logging.warning(
                        'SQL Object: %s ignored, metadata def: %s'
                        ' or query: %s dont exist', item_name,
                        metadata_def_full_path, query_full_path)

        return parsed_config

    def __get_content_dict_attribute(self, attribute_name):
        content_attribute = self._conf_content.get(attribute_name)

        if isinstance(content_attribute, dict):
            return content_attribute

        return None

    def __determine_scraping_steps(self):
        logging.info('\n\n==============Loading Config===============')

        if self._conf_content.get(constants.REFRESH_OPTION) is not None:
            self.refresh_metadata_tables = self._conf_content[
                constants.REFRESH_OPTION]

        options = self.get_chosen_metadata_options()

        self.sql_objects_config = self.__get_sql_objects_config()

        self.base_metadata_query = self.__get_base_metadata_query_config()

        if len(options):
            self.scrape_optional_metadata = True

    @classmethod
    def __read_yaml_file(cls, path):
        with open(path, 'r') as f:
            conf = config.yaml_config.YamlConfig.parse_as_dict(f)

        # needs to return an empty config since file may not exist.
        return conf or dict()

    @classmethod
    def __read_sql_query_file(cls, path):
        with open(path, 'r') as f:
            data = f.read()
            return data

    @classmethod
    def __read_json_file(cls, path):
        with open(path, 'r') as f:
            return json.load(f)

    @classmethod
    def __connector_has_config_files_for_sql_objects(cls, query_full_path,
                                                     metadata_def_full_path):
        return cls.__file_exists(query_full_path) and cls.__file_exists(
            metadata_def_full_path)

    @classmethod
    def __file_exists(cls, file_path):
        return os.path.exists(file_path)
