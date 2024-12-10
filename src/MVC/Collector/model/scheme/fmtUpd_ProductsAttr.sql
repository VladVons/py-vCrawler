-- fmtUpd_ProductsAttr.sql
-- in: aValues

update
  ref_product rp
set
  attr = src.attr,
  title_crc = hashtext(src.title)
from (
  values {{aValues}} 
) as src(url_id, title, attr)
where 
  rp.url_id = src.url_id
