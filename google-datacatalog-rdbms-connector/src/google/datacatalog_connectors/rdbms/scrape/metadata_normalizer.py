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

import pandas as pd
import six


class MetadataNormalizer:

    def __init__(self):
        pass

    @classmethod
    def to_metadata_dict(cls, metadata, metadata_definition):
        """
         Receives a Pandas dataframe and normalizes it by creating a dictionary
         with Table Container(Database/Schema) -> Tables -> Columns hierarchy.

         :param metadata: the Pandas dataframe
         :param metadata_definition: the Metadata Definition

         the normalized dictionary will be created with the specified
         target keys.

         Example:
            >>> metadata_definition = {
            ...        'table_container_def': {
            ...            'key': 'schemas',
            ...            'type': 'schema',
            ...            'name': 'schema_name',
            ...            'fields': [
            ...                {
            ...                    'source': 'schema_created',
            ...                    'target': 'create_time'
            ...                }
            ...            ]
            ...        },
            ...        'table_def': {
            ...            'key': 'tables',
            ...            'type': 'table',
            ...            'name': 'table_name',
            ...            'fields': [
            ...                {
            ...                    'source': 'table_comments',
            ...                    'target': 'desc'
            ...                }
            ...            ]
            ...        },
            ...        'column_def': {
            ...            'key': 'columns',
            ...            'type': 'column',
            ...            'name': 'column_name',
            ...            'fields': [
            ...                {
            ...                    'source': 'data_length',
            ...                    'target': 'length'
            ...                }
            ...            ]
            ...        }
            ...}


         :return: a normalized dict object
        """

        cls.__remove_nan_rows(metadata)

        table_container_def = metadata_definition['table_container_def']

        return {
            table_container_def['key']:
                cls.__normalize_objects(
                    metadata=metadata,
                    key_column_name=table_container_def['name'],
                    normalizer_method=cls.__normalize_table_container,
                    metadata_definition=metadata_definition)
        }

    @classmethod
    def __remove_nan_rows(cls, metadata):
        # Remove nan fields
        pd.options.mode.chained_assignment = None
        metadata.dropna(axis=0, how='all', inplace=True)

    @classmethod
    def __normalize_objects(cls, metadata, key_column_name, normalizer_method,
                            metadata_definition):
        """
         Generic method to normalize a Pandas dataframe
         into an array dictionary objects.

         :param metadata: the Pandas dataframe
         :param key_column_name: column used to
          distinguish top-level objects from each other
         :param normalizer_method: the method
          used to normalize each top-level object
         :param metadata_definition: the Metadata Definition

         :return: an array of normalized dict objects
        """

        metadata.set_index(key_column_name, inplace=True)

        key_values = metadata.index.unique().tolist()

        array = []
        for key_value in key_values:
            # We use an array with: [key_value] to make sure the dataframe loc
            # always returns a dataframe, and not a Series
            metadata_subset = metadata.loc[[key_value]]
            metadata.drop(key_value, inplace=True)
            array.append(
                normalizer_method(key_value.strip(), metadata_subset,
                                  metadata_definition))

        return array

    @classmethod
    def __normalize_table_container(cls, name, table_container_metadata,
                                    metadata_definition):

        tables_container_def = metadata_definition['table_container_def']
        fields = tables_container_def['fields']

        normalized_dict = {'name': name}

        normalized_dict.update(
            cls.__normalize_fields(fields, table_container_metadata))

        table_def = metadata_definition['table_def']

        normalized_dict[table_def['key']] = \
            cls.__normalize_objects(
             metadata=table_container_metadata.loc[
                      :, table_def['name']:],
             key_column_name=table_def['name'],
             normalizer_method=cls.__normalize_table,
             metadata_definition=metadata_definition
            )

        return normalized_dict

    @classmethod
    def __normalize_table(cls, name, table_metadata, metadata_definition):

        table_def = metadata_definition['table_def']
        fields = table_def['fields']

        normalized_dict = {'name': name}

        normalized_dict.update(cls.__normalize_fields(fields, table_metadata))

        column_def = metadata_definition['column_def']

        normalized_dict[column_def['key']] = cls.__normalize_objects(
            metadata=table_metadata.loc[:, column_def['name']:],
            key_column_name=column_def['name'],
            normalizer_method=cls.__normalize_column,
            metadata_definition=metadata_definition)
        return normalized_dict

    @classmethod
    def __normalize_column(cls, name, column_metadata, metadata_definition):

        column_def = metadata_definition['column_def']
        fields = column_def['fields']

        normalized_dict = {'name': name}

        normalized_dict.update(cls.__normalize_fields(fields, column_metadata))

        return normalized_dict

    @classmethod
    def __normalize_fields(cls, fields, metadata):
        fields_dict = {}
        for field in fields:
            source = field['source']
            target = field['target']

            # could be that optional information ('source')
            # is not present in scraped metadata
            if source in metadata:
                value = cls.__extract_value_from_first_row(metadata, source)

                if cls.__is_date_field(target):
                    value = cls.__normalize_timestamp_field(value)

                fields_dict[target] = value
        return fields_dict

    @classmethod
    def __extract_value_from_first_row(cls, df, column_name):
        value = df.iloc[0][column_name]

        if pd.isna(value):
            return value

        if isinstance(value, six.string_types):
            return value.strip()
        return value

    @classmethod
    def __normalize_timestamp_field(cls, timestamp_field):
        return pd.Timestamp(timestamp_field)

    @classmethod
    def __is_date_field(cls, target):
        # [TODO] Improve logic to identify timestamp fields
        # currently using a naming convention
        if '_date' in target or '_time' in target:
            return True

        return False

    @staticmethod
    def get_exact_table_names_from_dataframe(dataframe, metadata_definition):
        """
        Get table names in a form schema_name.table_name
        """
        container_name_col = metadata_definition['table_container_def']['name']
        table_name_col = metadata_definition['table_def']['name']
        container_table_pairs_df = dataframe[[
            container_name_col, table_name_col
        ]]
        container_table_pairs_records = container_table_pairs_df.to_dict(
            orient='records')
        exact_table_names = list()
        for pair_dict in container_table_pairs_records:
            values = [val.strip() for val in pair_dict.values()]
            exact_table_name = ".".join(values)
            exact_table_names.append(exact_table_name)
        return exact_table_names
