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

# User defined config keys
ENRICH_METADATA_OPTION = 'enrich_metadata'
BASE_METADATA_QUERY_FILENAME = 'base_metadata_query_filename'
REFRESH_OPTION = 'refresh_metadata_tables'
ROW_COUNT_OPTION = 'sync_row_counts'

# Metadata config keys
ASSET_NAME_KEY = 'name'
TABLE_CONTAINER_DEF_KEY = 'table_container_def'
TABLE_DEF_KEY = 'table_def'
COLUMN_DEF_KEY = 'column_def'

# Base Metadata fields
TABLE_TYPE_KEY = 'type'
VIEW_TYPE_VALUE = 'view'

# Metadata enrich attributes keys
METADATA_ENRICH_ENTRY_PREFIX = 'entry_prefix'
METADATA_ENRICH_ENTRY_ID_PATTERN_FOR_PREFIX = 'entry_id_pattern_for_prefix'

# Metadata scrape base entries
BASE_ENTRIES_KEY = 'base_entries'

# Metadata scrape sql objects
SQL_OBJECTS_KEY = 'sql_objects'
SQL_OBJECT_ITEM_NAME = 'name'

SQL_OBJECT_TYPE = 'type'
SQL_OBJECT_NAME = 'name'
SQL_OBJECT_ITEM_QUERY_KEY = 'query'
SQL_OBJECT_ITEM_QUERY_FILENAME_PREFIX = 'query'
SQL_OBJECT_ITEM_QUERY_FILENAME_SUFFIX = 'sql_object.sql'

SQL_OBJECT_ITEM_METADATA_DEF_KEY = 'metadata_def'
SQL_OBJECT_ITEM_METADATA_DEF_FILENAME_PREFIX = 'metadata_definition'
SQL_OBJECT_ITEM_METADATA_DEF_FILENAME_SUFFIX = 'sql_object.json'

SQL_OBJECT_ITEM_ENABLED_FLAG = 'enabled'

# Metadata scrape sql objects items
SQL_OBJECT_ITEMS_KEY = 'items'

# Metadata scrape sql objects model types
SQL_OBJECT_TAG_MODEL = 'tag'
SQL_OBJECT_ENTRY_MODEL = 'entry'

# Metadata scrape sql objects field types
SQL_OBJECT_DOUBLE_FIELD = 'double'
SQL_OBJECT_STRING_FIELD = 'string'
SQL_OBJECT_BOOLEAN_FIELD = 'bool'
SQL_OBJECT_TIMESTAMP_FIELD = 'timestamp'

# Metadata scrape sql objects fields
SQL_OBJECT_FIELDS = 'fields'
SQL_OBJECT_FIELD_TARGET = 'target'
SQL_OBJECT_FIELD_TARGET_DEFINITION = 'definition'
SQL_OBJECT_FIELD_TARGET_NAME = 'field_name'
SQL_OBJECT_FIELD_TARGET_MODEL = 'model'
SQL_OBJECT_FIELD_TARGET_TYPE = 'type'

# SQL Objects config tag fields names
SQL_OBJECT_CONFIG_FIELD_NAME = 'name'
SQL_OBJECT_CONFIG_FIELD_PURPOSE = 'purpose'
SQL_OBJECT_CONFIG_FIELD_INPUTS = 'inputs'
SQL_OBJECT_CONFIG_FIELD_OUTPUTS = 'outputs'

# Metadata scrape sql objects entry pre defined field
SQL_OBJECT_ENTRY_CREATE_TIME = 'create_time'
SQL_OBJECT_ENTRY_UPDATE_TIME = 'update_time'
SQL_OBJECT_ENTRY_DESCRIPTION = 'description'
