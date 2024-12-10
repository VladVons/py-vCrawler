-- fmtGet_ProductByUrlId.sq
-- in: aUrlId

select
  hu.url_id,
  hu.parsed_data as product,
  hu.create_date,
  rp.attr
from
  hist_url hu
join
  ref_product rp on rp.url_id = hu.url_id
where
  hu.url_id = {{aUrlId}}
order by
  hu.id desc
limit
  1
