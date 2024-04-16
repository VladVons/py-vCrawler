with wt1 as (
    select
        count(*) as cnt,
        url_id
    from hist_url
    group by url_id
)
select
    --(hu.parsed_data->>'stock')::bool,
    wt1.cnt,
    ru.site_id,
    ru.id as url_id,
    ru.url,
    hu.id as hist_id,
    hu.status_code,
    hu.create_date,
    hu.parsed_data
from
    ref_url ru
left join
    hist_url hu on
    (hu.url_id = ru.id)
left join
    wt1 on
    (wt1.url_id = ru.id)
where 
    (ru.site_id != 1) and
    --(url_id = 62043) and
    --((hu.parsed_data->>'stock')::bool) and
    (wt1.cnt > 1) and
    (hu.create_date is not null)
order by
    hu.create_date desc
--limit
--      1000
