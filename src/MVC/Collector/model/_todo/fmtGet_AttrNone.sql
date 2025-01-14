select
  category,
  lower(title),
  attr
from
  ref_product
where (
    select count(*)
    from jsonb_object_keys(attr)
) < 1
order by
  title
limit
  100

