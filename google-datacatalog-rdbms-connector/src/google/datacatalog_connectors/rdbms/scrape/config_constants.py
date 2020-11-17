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
REFRESH_OPTION = 'refresh_metadata_tables'
ROW_COUNT_OPTION = 'sync_row_counts'

# Metadata config keys
ASSET_NAME_KEY = 'name'
TABLE_CONTAINER_DEF_KEY = 'table_container_def'
TABLE_DEF_KEY = 'table_def'

# Metadata enrich attributes keys
METADATA_ENRICH_ENTRY_PREFIX = 'entry_prefix'
METADATA_ENRICH_ENTRY_ID_PATTERN_FOR_PREFIX = 'entry_id_pattern_for_prefix'

# Metadata scrape sql objects
SQL_OBJECTS_KEY = 'sql_objects'
SQL_OBJECT_ITEM_NAME = 'name'

SQL_OBJECT_ITEM_QUERY_KEY = 'query'
SQL_OBJECT_ITEM_QUERY_FILENAME_PREFIX = 'query'
SQL_OBJECT_ITEM_QUERY_FILENAME_SUFFIX = 'sql_object.sql'

SQL_OBJECT_ITEM_METADATA_DEF_KEY = 'metadata_def'
SQL_OBJECT_ITEM_METADATA_DEF_FILENAME_PREFIX = 'metadata_definition'
SQL_OBJECT_ITEM_METADATA_DEF_FILENAME_SUFFIX = 'sql_object.json'

SQL_OBJECT_ITEM_ENABLED_FLAG = 'enabled'
