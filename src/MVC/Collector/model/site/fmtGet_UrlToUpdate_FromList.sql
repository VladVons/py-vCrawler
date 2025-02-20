-- fmtGet_UrlToUpdate_FromList.sql
-- in: aSiteId, Urls

select
  ru.id as url_id,
  ru.url,
  ru.update_date,
  ru.url_en
from
  ref_site rs
left join
  ref_url ru on (ru.site_id = rs.id)
where
  (rs.id = {{aSiteId}}) and
  (ru.url in ({{Urls}})) and
  ((ru.unlock_date is null) or (ru.unlock_date < now())) and
  ((ru.update_date is null) or (ru.update_date < (now() - (rs.update_hours || ' hours')::interval)))
order by
  ru.update_date asc nulls first
