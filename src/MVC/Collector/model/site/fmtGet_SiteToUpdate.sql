-- fmtGet_SiteToUpdate.sql
-- rsp.scheme::text to save dict keys ordering

select
  rs.id,
  rs.url,
  rs.urls_parse,
  rs.sleep_seconds,
  rs.robots,
  rs.headers,
  rs.emulator,
  (
    select jsonb_agg(rsp.scheme::text)
    from ref_site_parser rsp
    where (rsp.moderated and rsp.site_id = rs.id)
  ) as scheme,
  (
    select array_agg(rsc.path)
    from ref_site_category rsc
    where (rsc.enabled and rsc.site_id = rs.id)
  ) as category
from
  ref_site rs
join
  ref_url ru on (ru.site_id = rs.id)
join
  ref_site_parser rsp on (rsp.site_id = rs.id) and (rsp.moderated) and (rsp.url_en = 'product')
where
  (rs.enabled) and
  ((rs.unlock_date is null) or (rs.unlock_date < now())) and
  ((ru.unlock_date is null) or (ru.unlock_date < now())) and
  ((ru.update_date is null) or (ru.update_date < (now() - (rs.update_hours || ' hours')::interval)))
order by
  ru.update_date asc nulls first
limit
  1
