select
    key, value,
    count(*) as count
from (
    select
        key, value
    from
        ref_product rp,
        jsonb_each_text(attr)
    where
        key not in ('model', 'brand')
) as kv_pairs
group by
    key, value
order by
    key, value
