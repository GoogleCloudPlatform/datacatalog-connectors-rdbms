#!/usr/bin/python
#
# Copyright 2021 Google LLC
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

from google.datacatalog_connectors.commons import config

# We use class imports here to improve the schema definition readability.
from schema import Schema, And, Optional


class SQLObjectsMetadataConfig:
    __METADATA_DEFINITION_KEY = 'metadata_definition'

    __schema = Schema(
        {
            __METADATA_DEFINITION_KEY: {
                'name': And(str),
                'purpose': And(str),
                Optional('inputs'): [{
                    'name': And(str),
                    'type': And(str)
                }],
                Optional('outputs'): [{
                    'name': And(str),
                    'type': And(str)
                }]
            }
        },
        ignore_extra_keys=True)

    def __init__(self, content):
        """
        Validates and creates the sql objects metadata config.
        Raises schema.SchemaError if the attributes don't match the schema.
        """
        parsed_config = config.yaml_config.YamlConfig.parse_as_dict(content)
        self.__schema.validate(parsed_config)
        self.__config = parsed_config

    def get_name(self):
        metadata_definition = self.__config.get(self.__METADATA_DEFINITION_KEY,
                                                {})
        return metadata_definition.get('name')

    def get_purpose(self):
        metadata_definition = self.__config.get(self.__METADATA_DEFINITION_KEY,
                                                {})
        return metadata_definition.get('purpose')

    def get_inputs_formatted(self):
        return self.__get_attribute_list_formatted('inputs')

    def get_outputs_formatted(self):
        return self.__get_attribute_list_formatted('outputs')

    def __get_attribute_list_formatted(self, attribute_name):
        """
        Formats an attribute list using the following pattern:
        {name} ({type}), {name} ({type})

        Such as: in1 (string), in2 (double)
        """
        metadata_definition = self.__config.get(self.__METADATA_DEFINITION_KEY,
                                                {})
        inputs = metadata_definition.get(attribute_name)

        if inputs:
            return ', '.join([
                '{} ({})'.format(item.get('name'), item.get('type'))
                for item in inputs
            ])
