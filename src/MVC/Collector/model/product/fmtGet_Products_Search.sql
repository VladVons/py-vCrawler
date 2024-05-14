-- fmtGet_Products_Search.sql
-- in: FilterRe, aOrder, aLimit, aOffset

select
    count(*) over() as total,
    rp.title,
from
    ref_product rp
where
    (
        (rp.title ilike all (values {{FilterRe}})) or
        (rp.category ilike all (values {{FilterRe}}))
    )
order by
    title
limit
    25
offset
    0
