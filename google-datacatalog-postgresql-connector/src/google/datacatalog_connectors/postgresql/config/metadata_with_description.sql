/*
* Extract catalog information from pg_catalog.
* Some Postgresql databases come without schema details in information schema
* This query uses various tables from pg_catalog to build a catalog of columns with appropriate details:
* - schema & table name
* - table type is BASE TABLE
* - column name
* - column default value
* - column nullable indicator
* - column type with comma replaced with underscore for import as csv file
* - description, as added with COMMENT SQL command
* - table size in mb
*
* Freely inspired from SO: https://stackoverflow.com/questions/20194806/how-to-get-a-list-column-names-and-datatypes-of-a-table-in-postgresql
*/

SELECT t.schemaname as schema_name,
       tablename as table_name, 'BASE TABLE' as table_type,
       column_name,
       CASE
           WHEN has_default and column_type not in ('bigserial', 'serial') THEN default_value
           ELSE null
        END as column_default_value,
       not(is_notnullable) as column_nullable,
       pg_catalog.replace(column_type, ',', '_') as column_type, -- replace comma for CSV export
       -- column_char_length, -- not supported in metadata definition
       -- column_numeric_precision, -- not supported in metadata definition
       -- column_enum_values, -- not supported in metadata definition
       description,
       table_size_mb
    FROM pg_catalog.pg_tables as t
        INNER JOIN (
	        SELECT
	            pg_class.relname as table_name,
		        pg_namespace.nspname as schema_name,
	            pg_attribute.attname as column_name,
	            CASE pg_attribute.atttypid
	    	        WHEN 'bigint'::regtype THEN 'bigserial'
	    	        WHEN 'int'::regtype THEN 'serial'
	    	        ELSE pg_catalog.format_type(pg_attribute.atttypid, pg_attribute.atttypmod)
	            END as column_type,
	            pg_attribute.attnotnull as is_notnullable,
	            pg_attribute.atthasdef as has_default,
	            pg_attrdef.adsrc as default_value,
                CAST (pg_total_relation_size(pg_class.oid) AS FLOAT) / 1024 / 1024 as table_size_mb,
	            pgd.description as description
	        FROM
	            pg_catalog.pg_attribute
	            INNER JOIN
	                pg_catalog.pg_class ON pg_class.oid = pg_attribute.attrelid
	            INNER JOIN
	                pg_catalog.pg_namespace ON pg_namespace.oid = pg_class.relnamespace
	            LEFT JOIN
		            pg_catalog.pg_attrdef on pg_class.oid = pg_attrdef.adrelid and pg_attribute.attnum = pg_attrdef.adnum
	            LEFT JOIN 
		            pg_catalog.pg_description pgd on pgd.objoid = pg_attribute.attrelid and pgd.objsubid = pg_attribute.attnum
	        WHERE
	            pg_attribute.attnum > 0
	            AND NOT pg_attribute.attisdropped
        ) as c on c.schema_name = t.schemaname and c.table_name = t.tablename
    WHERE t.schemaname NOT IN 
        ('pg_catalog', 'information_schema',
         'pg_toast', 'gp_toolkit', 'pg_internal')
    ORDER BY schema_name, table_name, column_name
