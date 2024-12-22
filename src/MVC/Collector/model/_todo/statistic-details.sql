select
    rs.id,
    rs.enabled,
    rs.url as site,
    (
        select count(*)
        from ref_url ru
        join ref_product rp on rp.url_id = ru.id
        where ru.site_id = rs.id and stock
    ) as stock,
    (
        select count(*)
        from ref_url ru
        join ref_product rp on rp.url_id = ru.id
        where ru.site_id = rs.id
    ) as product,
    (
        select count(*)
        from ref_url
        where site_id = rs.id
    ) as url,
    (
        select count(*)
        from ref_url ru
        join hist_url hu on hu.url_id = ru.id
        where ru.site_id = rs.id
    ) as history,
    (
        select count(*)
        from ref_site_category
        where enabled and site_id = rs.id
    ) as category,
    (
        select count(*)
        from ref_url
        where site_id = rs.id and status_code != 200
    ) as err
from
    ref_site rs
order by
    product
