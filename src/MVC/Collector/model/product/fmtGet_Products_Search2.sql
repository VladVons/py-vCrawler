-- fmtGet_Products_Search2.sql
-- in: Filter, aOrder, aLimit, aOffset

with wt1 as(
    select
        count(*) over() as total,
        rp.*
    from
        ref_product rp
    join
        ref_url ru on
        ru.id = rp.url_id
    where
        (ru.status_code = 200) and
        (rp.price > 0) and
        tsv_title @@ to_tsquery('simple', '{{aFilter}}')
    order by
        rp.stock desc,
        rp.price
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
