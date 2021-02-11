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

from schema import Schema, And, Optional


class SQLObjectsMetadataConfig:
    __schema = Schema(
        {
            'metadata_definition': {
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

    @classmethod
    def parse_as_dict(cls, content):
        parsed_config = yaml_config.YamlConfig.parse_as_dict(content)
        cls.__schema.validate(parsed_config)
        return parsed_config
