SELECT dc.db_name, stb.source_table_name, stb.enabled FROM public.slave_to_bq stb LEFT JOIN public.database_connection dc ON stb.db_id = dc.db_id;
