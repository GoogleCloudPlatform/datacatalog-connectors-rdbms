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

import os
import unittest

from google.datacatalog_connectors.commons_test import utils
from google.datacatalog_connectors.rdbms import prepare
import mock


@mock.patch('google.cloud.datacatalog_v1beta1.DataCatalogClient.entry_path')
class AssembledEntryFactoryTestCase(unittest.TestCase):
    __PROJECT_ID = 'test_project'
    __LOCATION_ID = 'location_id'
    __ENTRY_GROUP_ID = 'oracle'
    __MOCKED_ENTRY_PATH = 'mocked_entry_path'

    __METADATA_SERVER_HOST = 'metadata_host'
    __PREPARE_PACKAGE = 'google.datacatalog_connectors.rdbms.prepare'

    __MODULE_PATH = os.path.dirname(os.path.abspath(__file__))

    def setUp(self):
        # Right now this is working as a integration test.
        # [TODO] Improve this test by Mocking the
        # DataCatalogEntryFactory and DataCatalogTagFactory
        # dependencies.
        metadata_def = utils.Utils.get_metadata_def_obj(self.__MODULE_PATH)
        entry_factory = prepare.datacatalog_entry_factory. \
            DataCatalogEntryFactory(
                AssembledEntryFactoryTestCase.__PROJECT_ID,
                AssembledEntryFactoryTestCase.__LOCATION_ID,
                AssembledEntryFactoryTestCase.__METADATA_SERVER_HOST,
                AssembledEntryFactoryTestCase.__ENTRY_GROUP_ID,
                metadata_def
            )
        tag_factory = prepare.datacatalog_tag_factory.DataCatalogTagFactory(
            metadata_def)

        self.__assembled_entry_factory = prepare.assembled_entry_factory. \
            AssembledEntryFactory(
                AssembledEntryFactoryTestCase.__ENTRY_GROUP_ID,
                metadata_def, entry_factory,
                tag_factory)

        tag_templates_dict = {
            'oracle_schema_metadata': {},
            'oracle_table_metadata': {},
            'oracle_column_metadata': {}
        }

        self.__assembled_entry_factory_with_template = \
            prepare.assembled_entry_factory. \
            AssembledEntryFactory(
                AssembledEntryFactoryTestCase.__ENTRY_GROUP_ID,
                metadata_def,
                entry_factory,
                tag_factory,
                tag_templates_dict)

    def test_metadata_should_be_converted_to_datacatalog_entries(
            self, entry_path):  # noqa:E125
        entry_path.return_value = \
            AssembledEntryFactoryTestCase.__MOCKED_ENTRY_PATH

        entry_factory = self.__assembled_entry_factory

        schemas_metadata = utils.Utils.convert_json_to_object(
            self.__MODULE_PATH, 'metadata.json')

        prepared_entries = \
            entry_factory. \
            make_entries(schemas_metadata)

        schemas = schemas_metadata['schemas']

        # This is the size of the combination of tables and schemas metadata
        # The returned object contains a list of schema + a list of tables
        # for each schema
        expected_created_entries_len = \
            sum([len(schema_item['tables']) for schema_item in schemas],
                len(schemas))

        # This is the size of the entries created based on the metadata
        # The returned tuple contains 1 schema + a list of tables
        # related to the schema on each iteration
        created_entries_len = sum(
            [len(tables) for (schema, tables) in prepared_entries],
            len(prepared_entries))

        schema, tables = prepared_entries[0]
        self.assertEqual([], schema.tags)
        for table in tables:
            self.assertEqual([], table.tags)

        self.assertEqual(expected_created_entries_len, created_entries_len)
        self.__assert_created_entry_fields(prepared_entries)

    @mock.patch('{}.'.format(__PREPARE_PACKAGE) + 'datacatalog_tag_factory.' +
                'DataCatalogTagFactory.make_tag_for_table_container_metadata')
    @mock.patch('{}.datacatalog_tag_factory.'.format(__PREPARE_PACKAGE) +
                'DataCatalogTagFactory.make_tag_for_table_metadata')
    @mock.patch('{}.datacatalog_tag_factory.'.format(__PREPARE_PACKAGE) +
                'DataCatalogTagFactory.make_tags_for_columns_metadata')
    def test_with_tag_templates_should_be_converted_to_dc_entries_with_tags(  # noqa
            self, make_tags_for_columns_metadata, make_tag_for_table_metadata,
            make_tag_for_table_container_metadata, entry_path):
        entry_path.return_value = \
            AssembledEntryFactoryTestCase.__MOCKED_ENTRY_PATH

        entry_factory = \
            self.__assembled_entry_factory_with_template

        schema_metadata = utils.Utils.convert_json_to_object(
            self.__MODULE_PATH, 'metadata.json')

        prepared_entries = \
            entry_factory. \
            make_entries(schema_metadata)

        schemas = schema_metadata['schemas']

        # This is the size of the combination of tables and schemas metadata
        # The returned object contains a list of schema +
        # a list of tables for each schema
        expected_created_entries_len = \
            sum([len(schema_item['tables']) for schema_item in schemas],
                len(schemas))

        # This is the size of the entries created based on the metadata
        # The returned tuple contains 1 schema + a list
        # of tables related to the schema on each iteration
        created_entries_len = sum(
            [len(tables) for (schema, tables) in prepared_entries],
            len(prepared_entries))

        self.assertEqual(expected_created_entries_len, created_entries_len)
        self.__assert_created_entry_fields(prepared_entries)

        schema, tables = prepared_entries[0]
        self.assertEqual(1, len(schema.tags))
        for table in tables:
            self.assertEqual(1, len(table.tags))
        self.assertEqual(14, make_tag_for_table_metadata.call_count)
        self.assertEqual(14, make_tags_for_columns_metadata.call_count)
        self.assertEqual(4, make_tag_for_table_container_metadata.call_count)

    def test_should_be_converted_to_dc_entries_verify_all_fields(  # noqa
            self, entry_path):
        entry_path.return_value = \
            AssembledEntryFactoryTestCase.__MOCKED_ENTRY_PATH
        entry_factory = self.__assembled_entry_factory

        schema_metadata = utils.Utils.convert_json_to_object(
            self.__MODULE_PATH, 'metadata_one_table.json')

        prepared_entries = \
            entry_factory. \
            make_entries(schema_metadata)

        tables = prepared_entries[0][1]
        self.assertEqual(len(tables), 1)

        for schema, tables in prepared_entries:
            schema_entry = schema.entry
            self.assertEqual('CO', schema.entry_id)
            self.assertEqual('schema', schema_entry.user_specified_type)
            self.assertEqual(AssembledEntryFactoryTestCase.__MOCKED_ENTRY_PATH,
                             schema_entry.name)
            self.assertEqual('', schema_entry.description)
            self.assertEqual('metadata_host/CO', schema_entry.linked_resource)
            self.assertEqual('oracle', schema_entry.user_specified_system)

            for table in tables:
                table_entry = table.entry
                self.assertEqual('CO_CUSTOMERS', table.entry_id)
                # Assert specific fields for table
                self.assertEqual('table', table_entry.user_specified_type)
                self.assertEqual('oracle', table_entry.user_specified_system)
                self.assertEqual(
                    AssembledEntryFactoryTestCase.__MOCKED_ENTRY_PATH,
                    table_entry.name)
                self.assertEqual('metadata_host/CO/CUSTOMERS',
                                 table_entry.linked_resource)
                self.assertGreater(len(table_entry.schema.columns), 0)
                first_column = table_entry.schema.columns[0]
                self.assertEqual('NUMBER', first_column.type)
                self.assertEqual('CUSTOMER_ID', first_column.column)
                self.assertEqual('Auto-incrementing primary key',
                                 first_column.description)

                second_column = table_entry.schema.columns[1]
                self.assertEqual('VARCHAR2', second_column.type)
                self.assertEqual('EMAIL_ADDRESS', second_column.column)
                self.assertEqual(
                    'The email address the person'
                    ' uses to access the account', second_column.description)

                third_column = table_entry.schema.columns[2]
                self.assertEqual('VARCHAR2', third_column.type)
                self.assertEqual('FULL_NAME', third_column.column)
                self.assertEqual('What this customer is called',
                                 third_column.description)

    def test_should_be_converted_to_dc_entries_illegal_characters(  # noqa
            self, entry_path):
        entry_path.return_value = \
            AssembledEntryFactoryTestCase.__MOCKED_ENTRY_PATH
        entry_factory = self.__assembled_entry_factory

        schema_metadata = utils.Utils.convert_json_to_object(
            self.__MODULE_PATH, 'metadata_illegal_names.json')

        prepared_entries = \
            entry_factory. \
            make_entries(schema_metadata)

        tables = prepared_entries[0][1]
        self.assertEqual(len(tables), 1)

        for schema, tables in prepared_entries:
            schema_entry = schema.entry
            self.assertEqual(
                'CO_very_looooooooooooooooooooooooooooooooooooooooooooooooong',
                schema.entry_id)
            self.assertEqual('schema', schema_entry.user_specified_type)
            self.assertEqual(AssembledEntryFactoryTestCase.__MOCKED_ENTRY_PATH,
                             schema_entry.name)
            self.assertEqual('', schema_entry.description)
            self.assertEqual(
                'metadata_host/'
                'CO_very_looooooooooooooooooooooooooooooooooooooooooooooooong',
                schema_entry.linked_resource)
            self.assertEqual('oracle', schema_entry.user_specified_system)

            for table in tables:
                print(table.entry_id)
                table_entry = table.entry
                self.assertEqual(
                    'CO_very_looooooooooooooooooooooooooooooooooooooooooooooo'
                    'oong_CUS', table.entry_id)
                # Assert specific fields for table
                self.assertEqual('table', table_entry.user_specified_type)
                self.assertEqual('oracle', table_entry.user_specified_system)
                self.assertEqual(
                    AssembledEntryFactoryTestCase.__MOCKED_ENTRY_PATH,
                    table_entry.name)
                self.assertEqual(
                    'metadata_host/CO_$/'
                    '_very_loooooooooooooooooooooooooo'
                    'ooooooooooooooooooooooong'
                    '/CUSTOMERS_very_loooooooooooooooooo'
                    'oooooooooooooooooooooooong', table_entry.linked_resource)
                self.assertGreater(len(table_entry.schema.columns), 0)
                first_column = table_entry.schema.columns[0]
                self.assertEqual('NUMBER', first_column.type)
                self.assertEqual('CUSTOMER_ID_2', first_column.column)
                self.assertEqual('Auto-incrementing primary key',
                                 first_column.description)

    def test_should_be_converted_to_dc_entries_column_type_as_bytes(  # noqa
            self, entry_path):
        entry_path.return_value = \
            AssembledEntryFactoryTestCase.__MOCKED_ENTRY_PATH
        entry_factory = self.__assembled_entry_factory

        schema_metadata = utils.Utils.convert_json_to_object(
            self.__MODULE_PATH, 'metadata_column_type_as_bytes.json')

        # we can't set the bytes value directly in the JSON file
        # so for this test case, we just convert the str value
        # to the bytes representation.
        varchar_type = schema_metadata['schemas'][0]['tables'][0]['columns'][
            0]['type']
        schema_metadata['schemas'][0]['tables'][0]['columns'][0][
            'type'] = varchar_type.encode("utf-8")

        prepared_entries = \
            entry_factory. \
            make_entries(schema_metadata)

        tables = prepared_entries[0][1]
        self.assertEqual(len(tables), 1)

        for schema, tables in prepared_entries:
            schema_entry = schema.entry
            self.assertEqual('schema', schema_entry.user_specified_type)
            self.assertEqual(AssembledEntryFactoryTestCase.__MOCKED_ENTRY_PATH,
                             schema_entry.name)
            self.assertEqual('', schema_entry.description)
            self.assertEqual('oracle', schema_entry.user_specified_system)

            for table in tables:
                print(table.entry_id)
                table_entry = table.entry
                # Assert specific fields for table
                self.assertEqual('table', table_entry.user_specified_type)
                self.assertEqual('oracle', table_entry.user_specified_system)
                self.assertEqual(
                    AssembledEntryFactoryTestCase.__MOCKED_ENTRY_PATH,
                    table_entry.name)
                self.assertGreater(len(table_entry.schema.columns), 0)
                first_column = table_entry.schema.columns[0]
                self.assertEqual('varchar', first_column.type)
                self.assertEqual('CUSTOMER_ID_2', first_column.column)
                self.assertEqual('Auto-incrementing primary key',
                                 first_column.description)

    def test_schema_no_tables_should_be_converted_to_dc_entries(  # noqa
            self, entry_path):
        entry_path.return_value = \
            AssembledEntryFactoryTestCase.__MOCKED_ENTRY_PATH
        entry_factory = self.__assembled_entry_factory

        schema_metadata = utils.Utils.convert_json_to_object(
            self.__MODULE_PATH, 'metadata_no_tables.json')

        prepared_entries = \
            entry_factory. \
            make_entries(schema_metadata)

        schemas = schema_metadata['schemas']

        # In this case we should not have tables,
        # so tables length should be zero
        expected_created_tables_len = sum(
            [len(schema_item['tables']) for schema_item in schemas])
        self.assertEqual(0, expected_created_tables_len)
        expected_created_entries_len = expected_created_tables_len +\
            len(schema_metadata)

        # This is the size of the entries created based on the metadata
        # The returned tuple contains 1 schema + a list of tables
        # related to the schema on each iteration
        created_tables_len = sum(
            [len(tables) for (_, tables) in prepared_entries])
        self.assertEqual(0, created_tables_len)
        created_entries_len = created_tables_len + len(prepared_entries)

        self.assertEqual(expected_created_entries_len, created_entries_len)
        self.__assert_created_entry_fields(prepared_entries)

    def __assert_created_entry_fields(self, prepared_entries):
        for user_defined_schema, user_defined_tables in prepared_entries:
            schema_entry = user_defined_schema.entry
            self.__assert_required(user_defined_schema.entry_id,
                                   user_defined_schema.entry)

            # Assert specific fields for schema
            self.assertEqual('schema', schema_entry.user_specified_type)
            self.assertEqual('oracle', schema_entry.user_specified_system)
            self.assertEqual(AssembledEntryFactoryTestCase.__MOCKED_ENTRY_PATH,
                             schema_entry.name)
            self.assertIn(AssembledEntryFactoryTestCase.__METADATA_SERVER_HOST,
                          schema_entry.linked_resource)

            for user_defined_table in user_defined_tables:
                table_entry = user_defined_table.entry
                self.__assert_required(user_defined_table.entry_id,
                                       table_entry)
                self.assertIsNotNone(
                    table_entry.source_system_timestamps.create_time)
                self.assertIsNotNone(
                    table_entry.source_system_timestamps.update_time)
                # Assert specific fields for table
                self.assertEqual('table', table_entry.user_specified_type)
                self.assertEqual('oracle', table_entry.user_specified_system)
                self.assertEqual(
                    AssembledEntryFactoryTestCase.__MOCKED_ENTRY_PATH,
                    table_entry.name)
                self.assertIn(
                    AssembledEntryFactoryTestCase.__METADATA_SERVER_HOST,
                    table_entry.linked_resource)
                self.assertGreater(len(table_entry.schema.columns), 0)
                for column in table_entry.schema.columns:
                    self.assertIsNotNone(column.type)
                    self.assertIsNotNone(column.column)

    def __assert_required(self, entry_id, entry):
        self.assertIsNotNone(entry_id)
        self.assertIsNotNone(entry.user_specified_type)
        self.assertIsNotNone(entry.name)
        self.assertIsNotNone(entry.description)
        self.assertIsNotNone(entry.linked_resource)
