-- fmtGet_ProductsAttrCountry.sql
-- in: aCountryId, aLimit, aOffset, aFilter

select
  count(*) over() as total,
  rp.url_id,
  rp.update_date,
  rp.title,
  rp.attr,
  rp.stock,
  rp.price,
  rp.price_old,
  rp.image,
  ru.url
from
  ref_product rp
join
  ref_url ru on ru.id = rp.url_id
join
  ref_site rs on rs.id = ru.site_id and rs.country_id = {{aCountryId}}
where
  (rp.stock is true) and
  (rp.attr @> '{{aFilter}}')
order by
  {{aOrder}}
limit
  {{aLimit}}
offset
  {{aOffset}}
