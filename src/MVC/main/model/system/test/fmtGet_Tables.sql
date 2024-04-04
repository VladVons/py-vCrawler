-- fmtGet_Tables.sql

select
    table_schema,
    table_name
from
    information_schema.tables
where
    table_schema = '{{aSchema}}'
order by
    table_name
