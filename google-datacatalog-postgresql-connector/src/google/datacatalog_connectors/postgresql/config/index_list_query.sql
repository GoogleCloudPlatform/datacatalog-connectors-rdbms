SELECT pi.schemaname as schema_name,
       pi.tablename as table_name,
       string_agg(pi.indexname, ', ') as index_list
FROM pg_indexes pi
WHERE pi.schemaname = 'public'
GROUP BY pi.tablename, pi.schemaname;
