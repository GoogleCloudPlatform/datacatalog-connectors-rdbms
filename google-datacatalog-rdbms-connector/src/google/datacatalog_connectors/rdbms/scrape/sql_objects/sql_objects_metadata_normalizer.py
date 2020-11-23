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

from google.datacatalog_connectors.rdbms.scrape import MetadataNormalizer


class SQLObjectsMetadataNormalizer(MetadataNormalizer):

    @classmethod
    def normalize(cls, metadata, metadata_definition):
        """
         Receives a Pandas dataframe and normalizes it by creating a dictionary
         with SQL Objects List.

         :param metadata: the Pandas dataframe
         :param metadata_definition: the Metadata Definition

         the normalized dictionary will be created with the specified
         target keys.

         Example:
            >>> metadata_definition = {
            ...                        "key": "functions",
            ...                        "type": "function",
            ...                        "name": "function_name",
            ...                        "fields": [
            ...                            {
            ...                                "source": "schema_name",
            ...                                "target": {
            ...                                    "field_name": "schema_name",
            ...                                    "model": "tag",
            ...                                    "type": "string"
            ...                                }
            ...                           },
            ...                            {
            ...                                "source": "definition",
            ...                                "target": {
            ...                                    "field_name": "definition",
            ...                                    "model": "tag",
            ...                                    "type": "string"
            ...                                }
            ...                            }
            ...                        ]
            ...                    }


         :return: a normalized dict object
        """

        cls._remove_nan_rows(metadata)

        return SQLObjectsMetadataNormalizer.__normalize_sql_objects(
            metadata, metadata_definition)

    @classmethod
    def __normalize_sql_objects(cls, metadata, metadata_definition):
        sql_object_type = metadata_definition['type']

        normalized_sql_object = {'type': sql_object_type}

        sql_object_name = metadata_definition['name']

        normalized_sql_object['items'] = cls._normalize_objects(
            metadata=metadata,
            key_column_name=sql_object_name,
            normalizer_method=cls.__normalize_sql_object,
            metadata_definition=metadata_definition)

        return normalized_sql_object

    @classmethod
    def __normalize_sql_object(cls, name, sql_objects_metadata,
                               metadata_definition):

        fields = metadata_definition['fields']

        normalized_dict = {'name': name}

        normalized_dict.update(
            cls._normalize_fields(fields, sql_objects_metadata))

        return normalized_dict

    @classmethod
    def _normalize_fields(cls, fields, metadata):
        fields_dict = {}
        for field in fields:
            source = field['source']
            target = field['target']

            target_name = target['field_name']

            # The 'source' field is optional and might not be present
            # in the scraped metadata.
            if source in metadata:
                value = cls._extract_value_from_first_row(metadata, source)

                if cls._is_timestamp_field(target):
                    value = cls._normalize_timestamp_field(value)

                fields_dict[target_name] = value

        return fields_dict

    @classmethod
    def _is_timestamp_field(cls, target):
        return 'timestamp' == target['type']
