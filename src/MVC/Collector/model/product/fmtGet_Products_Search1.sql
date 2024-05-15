-- fmtGet_Products_Search.sql
-- in: FilterRe, aOrder, aLimit, aOffset

with wt1 as(
    select
        count(*) over() as total,
        rp.*
    from
        ref_product rp
    where
        (
            (rp.title ilike all (values {{FilterRe}}))
        )
    order by
        price
    limit
        {{aLimit}}
    offset
        {{aOffset}}
)

select 
    wt1.*,
    ru.url,
    hu.create_date::date
from 
    wt1
join
    ref_url ru on 
    (ru.id = wt1.url_id)
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

) hu on hu.url_id = wt1.url_id
