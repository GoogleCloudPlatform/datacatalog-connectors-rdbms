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

SELECT  s.SCHEMA_NAME as schema_name,
        s.SCHEMA_OWNER as schema_owner,
        s.CREATE_TIME as schema_create_time,
        t.TABLE_NAME as table_name,
        t.COMMENTS as table_description,
        t.TABLE_TYPE as table_type,
        t.HAS_PRIMARY_KEY as has_primary_key,
        t.CREATE_TIME as table_create_time,
        c.COLUMN_NAME as column_name,
        c.DATA_TYPE_NAME as column_type,
        c.IS_NULLABLE as column_nullable,
        c.COMMENTS as column_description,
        c.IS_MASKED as column_mask,
        c.MASK_EXPRESSION as column_mask_expression
      FROM SYS.SCHEMAS s
          JOIN  SYS.TABLES t
          on t.SCHEMA_NAME = s.SCHEMA_NAME
          JOIN  SYS.TABLE_COLUMNS c
          on c.TABLE_OID = t.TABLE_OID
      WHERE s.SCHEMA_NAME NOT IN (
          'SYS', '_SYS_BI', '_SYS_EPM', '_SYS_REPO',
          '_SYS_RT', 'SAP_PA_APL', 'SAP_XS_LM_PE',
          '_SYS_AFL', '_SYS_DI', '_SYS_STATISTICS',
          'SAP_REST_API', 'UIS', '_SYS_BIC',
          'HANA_XS_BASE', '_SYS_WORKLOAD_REPLAY',
          '_SYS_PLAN_STABILITY', '_SYS_TELEMETRY',
          '_SYS_SECURITY', '_SYS_AUDIT',
          '_SYS_TASK', '_SYS_XS', 'SAP_XS_LM',
          'SAP_XS_USAGE', '_SYS_DATA_ANONYMIZATION',
          '_SYS_SQL_ANALYZER')
      AND t.TABLE_NAME NOT IN (
          'SYS_AFL_GENERATOR_PARAMETERS'
      )
  ORDER BY s.SCHEMA_NAME, t.TABLE_NAME, c.COLUMN_NAME;