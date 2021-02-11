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

from google.datacatalog_connectors.commons.config import yaml_config
from google.datacatalog_connectors.rdbms.common import constants

from schema import Schema, And, Optional


class SQLObjectsMetadataConfig:
    __schema = Schema(
        {
            constants.SQL_OBJECT_CONFIG_FIELD_METADATA_DEFINITION: {
                constants.SQL_OBJECT_CONFIG_FIELD_NAME:
                    And(str),
                constants.SQL_OBJECT_CONFIG_FIELD_PURPOSE:
                    And(str),
                Optional(constants.SQL_OBJECT_CONFIG_FIELD_INPUTS): [{
                    constants.SQL_OBJECT_CONFIG_FIELD_INOUT_NAME: And(str),
                    constants.SQL_OBJECT_CONFIG_FIELD_INOUT_TYPE: And(str)
                }],
                Optional(constants.SQL_OBJECT_CONFIG_FIELD_OUTPUTS): [{
                    constants.SQL_OBJECT_CONFIG_FIELD_INOUT_NAME: And(str),
                    constants.SQL_OBJECT_CONFIG_FIELD_INOUT_TYPE: And(str)
                }]
            }
        },
        ignore_extra_keys=True)

    def __init__(self, content):
        """
        Validates and creates the sql objects metadata config.
        Raises schema.SchemaError if the attributes don't match the schema.
        """
        parsed_config = yaml_config.YamlConfig.parse_as_dict(content)
        self.__schema.validate(parsed_config)
        self.__config = parsed_config

    def get_name(self):
        metadata_definition = self.__config.get(
            constants.SQL_OBJECT_CONFIG_FIELD_METADATA_DEFINITION, {})
        return metadata_definition.get(constants.SQL_OBJECT_CONFIG_FIELD_NAME)

    def get_purpose(self):
        metadata_definition = self.__config.get(
            constants.SQL_OBJECT_CONFIG_FIELD_METADATA_DEFINITION, {})
        return metadata_definition.get(
            constants.SQL_OBJECT_CONFIG_FIELD_PURPOSE)

    def get_inputs_formatted(self):
        return self.__get_attribute_list_formatted(
            constants.SQL_OBJECT_CONFIG_FIELD_INPUTS)

    def get_outputs_formatted(self):
        return self.__get_attribute_list_formatted(
            constants.SQL_OBJECT_CONFIG_FIELD_OUTPUTS)

    def __get_attribute_list_formatted(self, attribute_name):
        """
        Formats an attribute list using the following pattern:
        {name} ({type}),{name}  ({type} )

        Such as: in1 (string),in2 (double)
        """
        metadata_definition = self.__config.get(
            constants.SQL_OBJECT_CONFIG_FIELD_METADATA_DEFINITION, {})
        inputs = metadata_definition.get(attribute_name)

        if inputs:
            return ','.join([
                '{} ({})'.format(
                    item.get(constants.SQL_OBJECT_CONFIG_FIELD_INOUT_NAME),
                    item.get(constants.SQL_OBJECT_CONFIG_FIELD_INOUT_TYPE))
                for item in inputs
            ])
