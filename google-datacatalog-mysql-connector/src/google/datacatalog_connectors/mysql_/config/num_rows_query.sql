SELECT  t.table_schema as database_name,
        t.table_name, t.table_rows

      FROM information_schema.tables t

      WHERE t.table_schema NOT IN
          ('mysql', 'information_schema',
           'performance_schema', 'sys')
      ORDER BY t.table_name;