-- fmtGet_ProductByUrlId.sql
-- in: aUrlIds

 select
  hu.url_id,
  hu.parsed_data as product,
  hu.create_date,
  rp.attr,
  ru.url,
  rs.id as site_id,
  rs.country_id
from
  hist_url hu
join
  ref_product rp on (rp.url_id = hu.url_id)
join
  ref_url ru on (ru.id = hu.url_id)
join
  ref_site rs on (rs.id = ru.site_id) and (rs.enabled is true)
where
  -hu.id in (
       select
         max(id)
       from
         hist_url
       where
         url_id = any (array[{{aUrlIds}}])
       group by
         url_id
    )
order by
    array_position(array[{{aUrlIds}}], hu.url_id)
