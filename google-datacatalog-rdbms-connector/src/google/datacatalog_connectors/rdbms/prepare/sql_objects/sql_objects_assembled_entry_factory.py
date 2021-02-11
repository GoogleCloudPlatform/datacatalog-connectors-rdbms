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

from google.datacatalog_connectors.commons import prepare

from google.datacatalog_connectors.rdbms.common import constants
from google.datacatalog_connectors.rdbms.prepare.sql_objects\
    import sql_objects_datacatalog_entry_factory,\
    sql_objects_datacatalog_tag_factory


class SQLObjectsAssembledEntryFactory:

    def __init__(self, project_id, location_id, entry_resource_url_prefix,
                 entry_group_id, sql_objects_config, tag_templates_dict):
        self.__entry_group_id = entry_group_id
        self.__sql_objects_config = sql_objects_config
        self.__tag_templates_dict = tag_templates_dict
        self.__datacatalog_entry_factory = \
            sql_objects_datacatalog_entry_factory.\
            SQLObjectsDataCatalogEntryFactory(
                project_id,
                location_id,
                entry_resource_url_prefix,
                self.__entry_group_id,
                self.__sql_objects_config)
        self.__datacatalog_tag_factory = sql_objects_datacatalog_tag_factory.\
            SQLObjectsDataCatalogTagFactory(sql_objects_config)

    def make_entries(self, sql_objects_metadata):
        assembled_entries = []
        if not sql_objects_metadata:
            return assembled_entries

        for sql_object_key, sql_object_metadata in\
                sql_objects_metadata.items():
            sql_object_type = sql_object_metadata[constants.SQL_OBJECT_TYPE]
            sql_object_items = sql_object_metadata[
                constants.SQL_OBJECT_ITEMS_KEY]
            for sql_object_item in sql_object_items:
                entry_id, entry = self.__datacatalog_entry_factory.\
                    make_entry_for_sql_object(
                        sql_object_key, sql_object_type, sql_object_item)

                tag_template_id = '{}_{}_metadata'.format(
                    self.__entry_group_id, sql_object_type)

                tag_template = self.__tag_templates_dict[tag_template_id]

                tags = self.__datacatalog_tag_factory.\
                    make_tags_for_sql_object(
                        sql_object_key, sql_object_item, tag_template)

                assembled_entries.append(
                    prepare.AssembledEntryData(entry_id, entry, tags))

        return assembled_entries
