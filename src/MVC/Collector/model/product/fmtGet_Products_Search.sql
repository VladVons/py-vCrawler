-- fmtGet_Products_Search.sql
-- in: FilterRe, aOrder, aLimit, aOffset

select
    count(*) over() as total,
    rp.*,
    ru.url 
from
    ref_product rp
join
    ref_url ru on 
    (ru.id = rp.url_id)
where
    (
        (rp.title ilike all (values {{FilterRe}}))
    )
order by
    title
limit
    {{aLimit}}
offset
    {{aOffset}}
