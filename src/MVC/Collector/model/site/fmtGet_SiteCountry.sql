-- fmtGet_SiteCountry.sql
-- in: aCountryId

select
  regexp_replace(url, '(://[^/]+).*', '\1') as url,
  regexp_replace(url, 'https?://(www\.)?([^/]+).*', '\2') as host,
  (select count(*) from ref_url where site_id = rs.id and url_en = 'product') as products,
  '' as info
from
  ref_site rs
where
  rs.country_id = {{aCountryId}}
order by
  host
