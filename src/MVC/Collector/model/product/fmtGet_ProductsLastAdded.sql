-- fmtGet_ProductsLastAdded.sql
-- in: aCountryId, aLimit

select
  *
from (
  select
    --rs.id as site_id,
    ru.id as url_id,
    ru.url,
    rp.update_date,
    rp.title,
    rp.image,
    rp.price,
    rp.price_old
  from
    ref_url ru
  join
    ref_site rs on rs.id =ru.site_id
  join
    ref_product rp on rp.url_id =ru.id
  where
    (rs.enabled is true) and
    (rs.country_id = {{aCountryId}}) and
    (ru.url_en = 'product') and
    (ru.status_code = 200) and
    (rp.stock is true) and
    (rp.price > 1000) and
    (rp.attr is not null and rp.attr <> '{}'::jsonb)
  order by
    ru.id desc
  limit
    {{aLimit}} * 3
) wt1
order by
  random()
limit
  {{aLimit}}
