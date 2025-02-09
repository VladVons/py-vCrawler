-- fmtGet_ProductsAttrSite.sql
-- in: aSiteId, aLimit, aOffset, aFilter

select
  count(*) over() as total,
  rp.url_id,
  rp.update_date,
  rp.title,
  rp.attr,
  rp.stock,
  rp.price,
  (rp.parsed_data->'price_old'->>0)::decimal as price_old,
  (rp.parsed_data->>'image') as image,
  ru.url
from
  ref_product rp
join
  ref_url ru on (ru.id = rp.url_id)
join
  ref_site rs on (rs.id = ru.site_id) and (rs.id = {{aSiteId}}) and (rs.enabled is true)
where
  (rp.stock is true) and
  (rp.attr @> '{{aFilter}}')
order by
  {{aOrder}}
limit
  {{aLimit}}
offset
  {{aOffset}}
