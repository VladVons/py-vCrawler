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
    select jsonb_agg(
      case
        when rsp.scheme::jsonb ? 'site_id'
          then master.scheme::text
          else rsp.scheme::text
      end
    )
    from ref_site_parser rsp
    left join ref_site_parser master on (rsp.scheme->>'site_id')::int = master.site_id
    where (rsp.moderated and rsp.site_id = rs.id)
  ) as scheme,
  (
    select array_agg(rsc.path)
    from ref_site_category rsc
    where (rsc.enabled and rsc.site_id = rs.id)
  ) as category,
  (
    select jsonb_build_object(
      'id', rp.id,
      'scheme', rp.scheme_en,
      'host', rp.host,
      'port', rp.port,
      'login', rp.login,
      'passw', rp.passw,
      'total',  count(*) over(),
      'required', rs.proxy
    )
    from ref_proxy rp
    where (rp.country_id = rs.country_id) and (rp.enabled is true) and (rp.valid_date >= now())
    order by random()
    limit 1
  ) as proxy
from
  ref_site rs
join
  ref_url ru on (ru.site_id = rs.id)
join
  ref_site_parser rsp on (rsp.site_id = rs.id) and (rsp.moderated) and (rsp.url_en = 'product' or rsp.url_en = 'prodcat')
where
  (rs.enabled is true) and
  ((rs.unlock_date is null) or (rs.unlock_date < now())) and
  ((ru.unlock_date is null) or (ru.unlock_date < now())) and
  ((ru.update_date is null) or (ru.update_date < (now() - (rs.update_hours || ' hours')::interval)))
order by
  ru.update_date asc nulls first
limit
  1
