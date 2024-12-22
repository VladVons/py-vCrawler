-- fmtGet_ProductByUrlId.sq
-- in: aUrlId

select
  hu.url_id,
  hu.parsed_data as product,
  hu.create_date,
  rp.attr,
  ru.url,
  rs.id as site_id,
  rs.country_id
from
  hist_url hu
join
  ref_product rp on (rp.url_id = hu.url_id)
join
  ref_url ru on (ru.id = hu.url_id)
join
  ref_site rs on (rs.id = ru.site_id)
where
  (hu.url_id = {{aUrlId}})
order by
  hu.id desc
limit
  1
