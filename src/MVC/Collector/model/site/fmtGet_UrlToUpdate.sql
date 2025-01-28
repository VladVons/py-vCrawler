-- fmtGet_UrlToUpdate.sql
--in: aSiteId, aLimit

select
  rs.id as site_id,
  ru.id as url_id,
  ru.url,
  ru.url_en,
  ru.update_date,
  rp.crc
from
  ref_site rs
join
  ref_url ru on (ru.site_id = rs.id)
join
  ref_product rp on (rp.url_id = ru.id)
where
  (rs.enabled is true) and
  (rs.id = {{aSiteId}}) and
  ((ru.unlock_date is null) or (ru.unlock_date < now())) and
  ((ru.update_date is null) or (ru.update_date < (now() - (rs.update_hours || ' hours')::interval)))
order by
  ru.update_date asc nulls first,
  ru.url
limit
  {{aLimit}}
