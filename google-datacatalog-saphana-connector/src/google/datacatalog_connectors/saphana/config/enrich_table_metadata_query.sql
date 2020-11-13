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

SELECT t.SCHEMA_NAME as schema_name,
       t.TABLE_NAME as table_name,
       t.RECORD_COUNT as table_rows,
       CAST (TABLE_SIZE AS FLOAT) / 1024 / 1024 as table_size_mb
    FROM SYS.M_TABLES t
      WHERE t.SCHEMA_NAME NOT IN (
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
    ORDER BY t.TABLE_NAME;