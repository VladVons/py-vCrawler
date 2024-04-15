-- fmtGet_HistUrlLast.sql

select
    ru.url, hu.*
from
    ref_url ru
join lateral (
    select
        data_size,
        url_id,
        url_count,
        status_code,
        parsed_data,
        create_date
    from
        hist_url
    where
        url_id = ru.id
    order by
        id desc
    limit 1

) hu on hu.url_id = ru.id
where
    (ru.site_id = {{aSiteId}})
