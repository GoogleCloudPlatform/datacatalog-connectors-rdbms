SELECT OBJECT_NAME(t.parent_id) as table_or_view_name,
       t.name as trigger_name,
       t.is_disabled as is_disabled,
       m.definition as definition
FROM sys.triggers t
JOIN sys.objects o ON o.name = t.name
JOIN sys.sql_modules m ON m.object_id = o.object_id
WHERE t.parent_class_desc = 'OBJECT_OR_COLUMN'
  AND o.type = 'TR';