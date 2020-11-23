SELECT specific_catalog as database_name,
       specific_schema as schema_name,
       routine_name as function_name,
       sql_data_access as sql_data_access,
       created as create_time,
       last_altered as update_time,
       routine_definition as definition
FROM   information_schema.routines 
WHERE  routine_type = 'function'
       AND LEFT(routine_name, 3) NOT IN( 'sp_', 'xp_', 'ms_' ); 