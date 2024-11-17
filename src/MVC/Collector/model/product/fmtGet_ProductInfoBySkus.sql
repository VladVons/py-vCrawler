-- fmtGet_ProductInfoBySkus.sql
-- in: aSiteId, Skus

select
    rp.sku,
    hu.parsed_data,
    ru.update_date
from
    ref_product rp
join
    ref_url ru on
    (ru.id =rp.url_id)
join lateral (
    select url_id, status_code, parsed_data
    from hist_url
    where (url_id = rp.url_id)
    order by id desc
    limit 1
) hu on hu.url_id = rp.url_id
where
    (rp.sku in ({{Skus}})) and
    (ru.site_id = {{aSiteId}}) and
    (hu.status_code = 200)
