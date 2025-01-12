-- fmtGet_ProductsAttrId.sql
-- in: aUrlIds, aLimit, aOffset

select
  count(*) over() as total,
  rp.url_id,
  rp.update_date,
  rp.title,
  rp.attr,
  rp.stock,
  rp.price,
  rp.price_old,
  rp.image,
  ru.url
from
  ref_product rp
join
  ref_url ru on (ru.id = rp.url_id)
where
  (rp.stock is true) and
  (rp.url_id in ({{aUrlIds}}))
limit
  {{aLimit}}
offset
  {{aOffset}}
