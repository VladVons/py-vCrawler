-- fmtGet_Conf.sql
-- in: aWhere

select
    jsonb_object_agg(attr,
        case
            when val_en = 'bool'  then to_jsonb(val::boolean)
            when val_en = 'int'   then to_jsonb(val::integer)
            when val_en = 'float' then to_jsonb(val::float)
            when val_en = 'text'  then to_jsonb(val)
            when val_en = 'json'  then val::jsonb
            when val_en = 'array' then to_jsonb(string_to_array(val, ','))
        end
    ) as val
from
  ref_conf
where
  {{WhereExt}}
