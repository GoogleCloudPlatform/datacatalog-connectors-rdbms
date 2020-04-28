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

from google.datacatalog_connectors.commons import prepare


class AssembledEntryFactory:

    def __init__(self,
                 entry_group_id,
                 metadata_definition,
                 datacatalog_entry_factory,
                 datacatalog_tag_factory,
                 tag_templates_dict=None):
        self.__datacatalog_entry_factory = datacatalog_entry_factory
        self.__datacatalog_tag_factory = datacatalog_tag_factory
        self.__entry_group_id = entry_group_id
        self.__metadata_definition = metadata_definition
        self.__tag_templates_dict = tag_templates_dict

    def make_entries_from_table_container_metadata(self, metadata):
        assembled_entries = []
        table_container_def = self.__metadata_definition['table_container_def']
        table_containers = metadata[table_container_def['key']]
        for table_container in table_containers:
            assembled_table_container = \
                self.__make_entries_for_table_container(
                    table_container)

            logging.info('\n--> %s: %s', table_container_def['type'],
                         table_container['name'].capitalize())
            logging.info('\n%s tables ready to be ingested...',
                         len(table_container['tables']))
            assembled_tables = self.__make_entry_for_tables(
                table_container['tables'], table_container['name'])

            assembled_entries.append(
                (assembled_table_container, assembled_tables))
        return assembled_entries

    def __make_entries_for_table_container(self, table_container):
        entry_id, entry = \
            self.__datacatalog_entry_factory.make_entries_for_table_container(
                table_container)

        tags = []
        if self.__tag_templates_dict:
            tag_template_id = '{}_{}_metadata'.format(
                self.__entry_group_id,
                self.__metadata_definition['table_container_def']['type'])
            tag_template = self.__tag_templates_dict[tag_template_id]
            tags.append(
                self.__datacatalog_tag_factory.
                make_tag_for_table_container_metadata(tag_template,
                                                      table_container))

        return prepare.AssembledEntryData(entry_id, entry, tags)

    def __make_entry_for_tables(self, tables, table_container_name):
        entries = []
        for table_dict in tables:
            entry_id, entry = self.__datacatalog_entry_factory. \
                make_entry_for_tables(table_dict, table_container_name)

            tags = []
            if self.__tag_templates_dict:
                tag_template_id = '{}_{}_metadata'.format(
                    self.__entry_group_id,
                    self.__metadata_definition['table_def']['type'])
                tag_template = self.__tag_templates_dict[tag_template_id]
                tags.append(
                    self.__datacatalog_tag_factory.make_tag_for_table_metadata(
                        tag_template, table_dict, table_container_name))

            entries.append(prepare.AssembledEntryData(entry_id, entry, tags))
        return entries
