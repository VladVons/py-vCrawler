-- fmtGet_Products_Search1.sql
-- in: FilterRe, aCountryId, aOrder, aLimit, aOffset

with wt1 as(
    select
        count(*) over() as total,
        rp.*
    from
        ref_product rp
    join
        ref_url ru on
        ru.id = rp.url_id
    join
        ref_site rs on
        rs.id = ru.site_id
    where
        (rs.country_id = {{aCountryId}}) and
        (rp.stock) and
        (rp.price > 0) and
        (rp.title ilike all (values {{FilterRe}}))
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
