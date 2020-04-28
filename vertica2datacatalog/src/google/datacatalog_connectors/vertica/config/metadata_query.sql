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

SELECT
    d.database_name as database_name,
    d.database_id as database_id,
    d.owner_name as database_owner,
    d.start_time as database_start_time,

    s.schema_name as schema_name,
    s.schema_id as schema_id,
    s.schema_owner as schema_owner,
    s.create_time as schema_create_time,

    t.table_name as table_name,
    t.table_id as table_id,
    t.owner_name as table_owner,
    t.create_time as table_create_time,

    c.column_name as column_name,
    c.column_id as column_id,
    c.data_type as column_type,
    c.data_type_length as column_length,
    c.column_default as column_default_value,
    c.is_nullable as column_nullable,
    c.numeric_precision as column_numeric_precision,
    c.numeric_scale as column_numeric_scale

FROM v_catalog.databases d,
    v_catalog.schemata s
    JOIN v_catalog.tables t ON t.table_schema_id = s.schema_id
    JOIN v_catalog.columns c ON c.table_id = t.table_id

WHERE (s.is_system_schema = 'f')
    AND s.schema_name NOT IN ('v_func', 'v_txtindex')

ORDER BY d.database_name, s.schema_name, t.table_name, c.column_name;
