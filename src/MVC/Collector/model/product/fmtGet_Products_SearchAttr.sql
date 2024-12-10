-- fmtGet_Products_SearchAttr.sql
-- in: aCountryId, aLimit, aOffset, aFilter

select
  rp.title,
  rp.attr,
  rp.stock,
  rp.price
from
  ref_product rp
join
  ref_url ru on ru.id = rp.url_id
join
  ref_site rs on rs.id = ru.site_id and rs.country_id = {{aCountryId}}
where
  rp.stock and
  rp.attr @> '{{aFilter}}'
order by
  {{aOrder}}
limit
  {{aLimit}}
offset
  {{aOffset}}
