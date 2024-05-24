-- fmtGet_Products_Search1.sql
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
    ru.url
from 
    wt1
join
    ref_url ru on 
    (ru.id = wt1.url_id)
