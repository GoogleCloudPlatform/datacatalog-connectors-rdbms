SELECT t.table_schema as schema_name,
       t.table_name,
       pc.reltuples as table_rows
    FROM information_schema.tables t
        JOIN pg_class pc
        on pc.relname = t.table_name
    WHERE t.table_schema NOT IN
        ('pg_catalog', 'information_schema',
         'pg_toast', 'gp_toolkit', 'pg_internal')
    ORDER BY t.table_name;