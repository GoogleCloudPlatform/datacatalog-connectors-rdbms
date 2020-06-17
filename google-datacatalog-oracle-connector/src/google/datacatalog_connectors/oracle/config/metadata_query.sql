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

select
     tab.owner as schema_name,
     schema.created as schema_create_time,
     tab.table_name as table_name,
     obj.object_type as table_type,
     obj.created table_create_time,
     obj.last_ddl_time as table_update_time,
     tab.num_rows as table_rows,
     tab_comm.comments as table_comments,
     col.column_name,
     col.data_type,
     decode(char_length,
            0, data_type,
            data_type || '(' || char_length || ')')
            as data_type_ext,
     col.data_length,
     col.data_precision,
     col.data_scale,
     col_comm.comments as col_comments,
     col.nullable
from all_tables tab
     inner join all_objects obj
         on obj.owner = tab.owner
        and obj.object_name = tab.table_name
     inner join all_users schema
         on schema.username = tab.owner
     left outer join all_tab_comments tab_comm
         on tab.table_name = tab_comm.table_name
        and tab.owner = tab_comm.owner
     inner join all_tab_columns col
        on col.owner = tab.owner
        and col.table_name = tab.table_name
     left join all_col_comments col_comm
         on col.owner = col_comm.owner
         and col.table_name = col_comm.table_name
         and col.column_name = col_comm.column_name
where tab.owner in
  (select username from all_users
   where oracle_maintained = 'N')
order by tab.owner,
     tab.table_name,
     col.column_name