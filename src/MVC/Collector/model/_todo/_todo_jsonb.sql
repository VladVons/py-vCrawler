--select keys
select *
from ref_product
where attr ?| array['case', 'cpu/family'];


-- delete keys
update ref_product
set attr = attr - array['pink', 'key2']
where attr ?| array['pink', 'key2']


-- to lower all string values
update ref_product
set attr = (
    select jsonb_object_agg(key,
        case
            when jsonb_typeof(attr->key) = 'string'
            then to_jsonb(lower((attr->>key)))
            else attr->key
        end
    )
    from jsonb_object_keys(attr) as keys(key)
)
where attr is not null


-- rename keys
update ref_product
set attr = (
    select jsonb_object_agg(
        case
            when key = 'old_key1' then 'new_key2'
            when key = 'old_key2' then 'new_key2'
            else key
        end,
        value
    )
    from jsonb_each(attr)
)
where attr ? 'old_key1' or attr ? 'old_key2';


-- update empty image from json field
update
  ref_product
set
  image = left(rp.parsed_data->>'image', 256)
from
  ref_product as rp
where
  (ref_product.url_id = rp.url_id) and
  (ref_product.image is null) and
  (rp.parsed_data::jsonb ? 'image')
