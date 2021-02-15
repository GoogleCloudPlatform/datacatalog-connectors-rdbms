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

from google.cloud import datacatalog

from google.datacatalog_connectors.commons_test import utils
from google.datacatalog_connectors.rdbms.common import constants
from google.datacatalog_connectors.rdbms.prepare.sql_objects import \
    sql_objects_datacatalog_tag_template_factory


class DataCatalogSQLObjectsTagTemplateFactoryTestCase(unittest.TestCase):
    __MODULE_PATH = '{}/..'.format(os.path.dirname(os.path.abspath(__file__)))

    __BOOL_TYPE = datacatalog.FieldType.PrimitiveType.BOOL
    __DOUBLE_TYPE = datacatalog.FieldType.PrimitiveType.DOUBLE
    __STRING_TYPE = datacatalog.FieldType.PrimitiveType.STRING

    __PROJECT_ID = 'test_project'
    __LOCATION_ID = 'test_location'
    __ENTRY_GROUP_ID = 'my_entry_group'

    def test_make_tag_template_for_sql_objects_should_set_all_available_fields(
            self):
        metadata = \
            utils.Utils.convert_json_to_object(
                self.__MODULE_PATH,
                'metadata_with_sql_objects.json')['sql_objects']
        sql_objects_config = \
            utils.Utils.convert_json_to_object(self.__MODULE_PATH,
                                               'sql_objects_config.json')

        factory = sql_objects_datacatalog_tag_template_factory. \
            SQLObjectsDataCatalogTagTemplateFactory(
                self.__PROJECT_ID,
                self.__LOCATION_ID,
                self.__ENTRY_GROUP_ID,
                sql_objects_config
            )

        tag_templates_dict = \
            factory.make_tag_templates_for_sql_objects_metadata(metadata)

        function_template = tag_templates_dict[
            'my_entry_group_function_metadata']

        self.assertEqual('My Entry Group Function - Metadata',
                         function_template.display_name)

        self.assertEqual(
            'projects/test_project/locations/test_location/'
            'tagTemplates/my_entry_group_function_metadata',
            function_template.name)

        self.assertEqual(
            self.__STRING_TYPE,
            function_template.fields['owner_name'].type.primitive_type)
        self.assertEqual('Owner Name',
                         function_template.fields['owner_name'].display_name)

        self.assertEqual(
            self.__STRING_TYPE,
            function_template.fields['schema_name'].type.primitive_type)
        self.assertEqual('Schema Name',
                         function_template.fields['schema_name'].display_name)

        self.assertEqual(
            self.__DOUBLE_TYPE, function_template.
            fields['input_parameter_count'].type.primitive_type)
        self.assertEqual(
            'Input Parameter Count',
            function_template.fields['input_parameter_count'].display_name)

        self.assertEqual(
            self.__STRING_TYPE,
            function_template.fields['definition'].type.primitive_type)
        self.assertEqual('Definition',
                         function_template.fields['definition'].display_name)

        self.assertEqual(
            self.__BOOL_TYPE,
            function_template.fields['is_valid'].type.primitive_type)
        self.assertEqual('Is Valid',
                         function_template.fields['is_valid'].display_name)

        self.assertEqual(
            self.__DOUBLE_TYPE,
            function_template.fields['return_value_count'].type.primitive_type)
        self.assertEqual(
            'Return Value Count',
            function_template.fields['return_value_count'].display_name)

        stored_procedure_template = tag_templates_dict[
            'my_entry_group_stored_procedure_metadata']

        self.assertEqual('My Entry Group Stored Procedure - Metadata',
                         stored_procedure_template.display_name)

        self.assertEqual(
            'projects/test_project/locations/test_location/'
            'tagTemplates/my_entry_group_stored_procedure_metadata',
            stored_procedure_template.name)

        self.assertEqual(
            self.__STRING_TYPE,
            stored_procedure_template.fields['owner_name'].type.primitive_type)
        self.assertEqual(
            'Owner Name',
            stored_procedure_template.fields['owner_name'].display_name)

        self.assertEqual(
            self.__STRING_TYPE, stored_procedure_template.
            fields['schema_name'].type.primitive_type)
        self.assertEqual(
            'Schema Name',
            stored_procedure_template.fields['schema_name'].display_name)

        self.assertEqual(
            self.__DOUBLE_TYPE, stored_procedure_template.
            fields['input_parameter_count'].type.primitive_type)
        self.assertEqual(
            'Input Parameter Count', stored_procedure_template.
            fields['input_parameter_count'].display_name)

        self.assertEqual(
            self.__STRING_TYPE,
            stored_procedure_template.fields['definition'].type.primitive_type)
        self.assertEqual(
            'Definition',
            stored_procedure_template.fields['definition'].display_name)

        self.assertEqual(
            self.__BOOL_TYPE,
            stored_procedure_template.fields['is_valid'].type.primitive_type)
        self.assertEqual(
            'Is Valid',
            stored_procedure_template.fields['is_valid'].display_name)

        self.assertEqual(
            self.__DOUBLE_TYPE, stored_procedure_template.
            fields['return_value_count'].type.primitive_type)
        self.assertEqual(
            'Return Value Count', stored_procedure_template.
            fields['return_value_count'].display_name)

        self.assertEqual(
            self.__STRING_TYPE, stored_procedure_template.
            fields[constants.SQL_OBJECT_CONFIG_FIELD_NAME].type.primitive_type)
        self.assertEqual(
            'Name', stored_procedure_template.
            fields[constants.SQL_OBJECT_CONFIG_FIELD_NAME].display_name)

        self.assertEqual(
            self.__STRING_TYPE, stored_procedure_template.
            fields[constants.SQL_OBJECT_CONFIG_FIELD_PURPOSE].type.primitive_type)
        self.assertEqual(
            'Purpose', stored_procedure_template.
            fields[constants.SQL_OBJECT_CONFIG_FIELD_PURPOSE].display_name)

        self.assertEqual(
            self.__STRING_TYPE, stored_procedure_template.
            fields[constants.SQL_OBJECT_CONFIG_FIELD_INPUTS].type.primitive_type)
        self.assertEqual(
            'Inputs', stored_procedure_template.
            fields[constants.SQL_OBJECT_CONFIG_FIELD_INPUTS].display_name)

        self.assertEqual(
            self.__STRING_TYPE, stored_procedure_template.
            fields[constants.SQL_OBJECT_CONFIG_FIELD_OUTPUTS].type.primitive_type)
        self.assertEqual(
            'Outputs', stored_procedure_template.
            fields[constants.SQL_OBJECT_CONFIG_FIELD_OUTPUTS].display_name)
