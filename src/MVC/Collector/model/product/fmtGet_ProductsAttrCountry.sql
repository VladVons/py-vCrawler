-- fmtGet_ProductsAttrCountry.sql
-- in: aCountryId,aFilter, aPriceMin, aPriceMax, aLimit, aOffset


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
  ru.url,
  ru.create_date
from
  ref_product rp
join
  ref_url ru on (ru.id = rp.url_id)
join
  ref_site rs on (rs.id = ru.site_id) and (rs.enabled is true) and (rs.country_id = {{aCountryId}})
where
  (rp.stock is true) and
  (rp.price between {{aPriceMin}} and {{aPriceMax}}) and
  (rp.attr @> '{{aFilter}}')
order by
  {{aOrder}}
limit
  {{aLimit}}
offset
  {{aOffset}}
