-- fmtGet_ProductsNoAttr.sql

select
  url_id,
  title
from 
  ref_product
where 
  (title_crc is null) or (title_crc != hashtext(title))
order by
  random()
limit
  {{aLimit}}
