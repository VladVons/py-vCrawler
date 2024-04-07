-- fmtGet_UrlToUpdate.sql
-- in: aLimit

with wt1 as (
    {% include './fmtGet_UrlToUpdate.sql' %}
)

select
    ru.site_id,
    ru.id as url_id,
    ru.url
    --now() + (rs.sleep_seconds * {{aLimit}} || ' seconds')::interval as unlock_date
from
    wt1
join
    ref_url ru on
    (ru.id = wt1.url_id)
join
    ref_site rs on
    (rs.id = wt1.site_id)
where
    ru.site_id in (
        select site_id from wt1 limit 1
    )
limit
    {{aLimit}}
