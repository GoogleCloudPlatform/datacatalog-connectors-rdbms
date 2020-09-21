/*
* Copyright 2020 Google LLC
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*      http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*/

WITH enums AS (
    select
       n.nspname as enum_schema,
       t.typname as enum_name,
       STRING_AGG(e.enumlabel, ', ') as enum_values
    FROM pg_type t
        JOIN pg_enum e ON t.oid = e.enumtypid
        JOIN pg_catalog.pg_namespace n ON n.oid = t.typnamespace
    GROUP BY n.nspname, t.typname
)
SELECT t.table_schema as schema_name,
       t.table_name, t.table_type,
       c.column_name,
       c.column_default as column_default_value,
       c.is_nullable as column_nullable,
       CASE
           WHEN e.enum_values is not null THEN 'enum'
           WHEN e.enum_values is null AND c.data_type = 'USER-DEFINED' THEN 'user_defined'
           ELSE c.data_type
       END as column_type,
       c.character_maximum_length as column_char_length,
       c.numeric_precision as column_numeric_precision,
       e.enum_values as column_enum_values,
       CAST (pg_total_relation_size(pc.oid) AS FLOAT) / 1024 / 1024 as table_size_mb
    FROM information_schema.tables t
        JOIN  information_schema.columns c
        on c.table_name = t.table_name and c.table_schema = t.table_schema
        JOIN pg_class pc
        on pc.relname = t.table_name
        LEFT JOIN enums e on e.enum_schema = c.udt_schema and e.enum_name = c.udt_name
    WHERE t.table_schema NOT IN
        ('pg_catalog', 'information_schema',
         'pg_toast', 'gp_toolkit', 'pg_internal')
    ORDER BY t.table_name, c.column_name;