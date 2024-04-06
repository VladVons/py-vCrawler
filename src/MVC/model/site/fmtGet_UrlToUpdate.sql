-- fmtGet_UrlToUpdate.sql

select
    rs.id as site_id,
    ru.id as url_id,
    ru.update_date
from
    ref_site rs
left join
    ref_url ru on
    (ru.site_id = rs.id)
where
    (rs.enabled) and
    (ru.enabled) and
    ((rs.unlock_date is null) or (rs.unlock_date < now())) and
    ((ru.unlock_date is null) or (ru.unlock_date < now())) and
    ((ru.update_date is null) or (ru.update_date < (now() - (rs.update_hours || ' hours')::interval)))
order by
    ru.update_date asc nulls first
