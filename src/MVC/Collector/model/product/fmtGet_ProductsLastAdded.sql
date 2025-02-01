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
    rp.price,
    (rp.parsed_data->'price_old'->>0)::decimal as price_old,
    (rp.parsed_data->>'image') as image
  from
    ref_url ru
  join
    ref_site rs on rs.id =ru.site_id
  join
    ref_product rp on rp.url_id =ru.id
  where
    (rs.enabled is true) and
    (rs.country_id = {{aCountryId}}) and
    (ru.status_code = 200) and
    (rp.stock is true) and
    (rp.price > 1000) and
    (rp.attr is not null and rp.attr <> '{}'::jsonb) and
    (rp.parsed_data::jsonb ? 'image')
  order by
    ru.id desc
  limit
    {{aLimit}} * 3
) wt1
order by
  random()
limit
  {{aLimit}}
