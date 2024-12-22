-- fmtGet_ProductsRnd.sql
-- in: aLimit

select
  title
from
  ref_product rp
where
  (stock is true)
order
  by random()
limit
  {{aLimit}}
