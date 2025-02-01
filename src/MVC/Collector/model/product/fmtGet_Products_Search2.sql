-- fmtGet_Products_Search2.sql
-- in: Filter, aOrder, aLimit, aOffset

with wt1 as(
  select
    count(*) over() as total,
    rp.url_id,
    rp.update_date,
    rp.title,
    rp.attr,
    rp.stock,
    rp.price,
    (rp.parsed_data->'price_old'->>0)::decimal as price_old,
    (rp.parsed_data->>'image') as image
  from
    ref_product rp
  join
    ref_url ru on (ru.id = rp.url_id)
  join
    ref_site rs on (rs.id = ru.site_id) and (rs.enabled is true)
  where
    (rs.country_id = {{aCountryId}}) and
    (rp.stock is true) and
    (rp.price > 0) and
    (tsv_title @@ to_tsquery('simple', '{{aFilter}}'))
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
  ref_url ru on (ru.id = wt1.url_id)
