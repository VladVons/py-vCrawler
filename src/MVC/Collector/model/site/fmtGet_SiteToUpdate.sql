-- fmtGet_SiteToUpdate.sql

select
    rs.id,
    rs.url,
    rs.urls_parse,
    rs.sleep_seconds,
    rs.robots,
    rs.headers,
    rsp.scheme
from
    ref_site rs
left join
    ref_site_parser rsp on
    (rsp.site_id = rs.id) and (rsp.url_en = 'product')
left join
    ref_url ru on
    (ru.site_id = rs.id)
where
    (rs.enabled) and
    (rsp.moderated) and
    ((rs.unlock_date is null) or (rs.unlock_date < now())) and
    ((ru.unlock_date is null) or (ru.unlock_date < now())) and
    ((ru.update_date is null) or (ru.update_date < (now() - (rs.update_hours || ' hours')::interval)))
order by
    ru.update_date asc nulls first
limit
    1
