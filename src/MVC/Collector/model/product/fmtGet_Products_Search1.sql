-- fmtGet_Products_Search1.sql
-- in: FilterRe, aCountryId, aOrder, aLimit, aOffset

with wt1 as(
  select
    count(*) over() as total,
    rs.id as site_id,
    rp.url_id,
    rp.update_date,
    rp.title,
    rp.attr,
    rp.stock,
    rp.price,
    rp.parsed_data->'price' as price_a,
    rp.parsed_data->'price_old' as price_old_a,
    rp.parsed_data->'image' as image,
    ru.create_date
  from
    ref_product rp
  join
    ref_url ru on (ru.id = rp.url_id)
  join
    ref_site rs on (rs.id = ru.site_id) and (rs.enabled is true) and (rs.country_id = {{aCountryId}})
  where
    (rp.stock is true) and
    (rp.price > 0) and
    {{ExtWhere}}
  order by
    {{aOrder}}
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
