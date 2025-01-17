-- fmtGet_CountryLang.sql
-- in: aCountry

select
  rc.id as country_id,
  rc.lang_id,
  rcl.title
from
  ref_site rs
join
  ref_country rc on rc.id = rs.country_id
join
  ref_country_lang rcl on rcl.country_id = rs.country_id and rcl.lang_id = 1
where
  rcl.title ilike '{{aCountry}}'
group by
  rc.id,
  rcl.title
