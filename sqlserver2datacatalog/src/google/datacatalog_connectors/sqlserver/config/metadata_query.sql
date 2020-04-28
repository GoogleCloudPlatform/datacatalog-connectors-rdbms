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

SELECT  t.table_schema as schema_name,
        t.table_name,
        t.table_type,
        c.column_name,
        c.column_default as column_default_value,
        c.is_nullable as column_nullable,
        c.data_type as column_type,
        c.character_maximum_length as
        column_char_length,
        c.numeric_precision as
        column_numeric_precision
      FROM information_schema.tables t
          JOIN  information_schema.columns c
          on c.table_name = t.table_name
      WHERE t.table_schema NOT IN ('dbo')
      AND c.table_schema NOT IN ('dbo')
  ORDER BY t.table_name, c.column_name;