-- fmtGet_Products_Search2.sql
-- in: Filter, aOrder, aLimit, aOffset

with wt1 as(
    select
        count(*) over() as total,
        rp.*
    from
        ref_product rp
    where
        tsv_title @@ to_tsquery('simple', '{{aFilter}}')
    order by
        price
    limit
        {{aLimit}}
    offset
        {{aOffset}}
)

select 
    wt1.*,
    ru.url
from 
    wt1
join
    ref_url ru on 
    (ru.id = wt1.url_id)
