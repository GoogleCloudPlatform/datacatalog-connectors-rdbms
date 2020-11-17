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

from google.datacatalog_connectors.rdbms.scrape. \
    metadata_sql_object_normalizer import MetadataSQLObjectNormalizer

from google.datacatalog_connectors.rdbms.scrape \
    import config_constants


class MetadataSQLObjectsScraper:

    def __init__(self, main_scraper):
        self.main_scraper = main_scraper

    def scrape(self, config, connection_args):
        sql_objects = {}
        if config and config.sql_objects_config:
            sql_objects_config = config.sql_objects_config

            for sql_object_config in sql_objects_config:
                name = sql_object_config[config_constants.SQL_OBJECT_ITEM_NAME]
                metadata_def = sql_object_config[
                    config_constants.SQL_OBJECT_ITEM_METADATA_DEF_KEY]
                query = sql_object_config[
                    config_constants.SQL_OBJECT_ITEM_QUERY_KEY]

                logging.info(
                    'Scraping metadata for sql objects: {}'.format(name))

                dataframe = self.main_scraper.get_metadata_as_dataframe(
                    metadata_def, connection_args, query)

                try:
                    sql_objects[
                        name] = MetadataSQLObjectNormalizer.to_metadata_dict(
                            dataframe, metadata_def)
                except:
                    logging.exception(
                        'Failed to scrape sql object, ignoring: {}'.format(
                            name))

        return sql_objects
