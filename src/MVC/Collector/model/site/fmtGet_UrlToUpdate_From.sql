-- fmtGet_UrlToUpdate.sql
--in: aSiteId, aLimit

select
  rs.id as site_id,
  ru.id as url_id,
  ru.url
from
  ref_site rs
left join
  ref_url ru on (ru.site_id = rs.id)
where
  (rs.enabled is true) and
  (rs.id = {{aSiteId}}) and
  (ru.url_en = 'product') and
  ((ru.unlock_date is null) or (ru.unlock_date < now())) and
  ((ru.update_date is null) or (ru.update_date < (now() - (rs.update_hours || ' hours')::interval)))
order by
  ru.update_date asc nulls first
limit
  {{aLimit}}
