-- fmtGet_ProductByUrlId.sq
-- in: aUrlId

select
  rp.url_id,
  rp.parsed_data,
  rp.update_date,
  rp.attr,
  ru.url,
  rs.id as site_id,
  rs.country_id,
  rs.url as site_url
from
  ref_product rp
join
  ref_url ru on (ru.id = rp.url_id)
join
  ref_site rs on (rs.id = ru.site_id) and (rs.enabled is true)
where
  (rp.url_id = {{aUrlId}})
