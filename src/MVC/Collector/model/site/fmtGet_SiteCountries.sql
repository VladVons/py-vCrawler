-- fmtGet_SiteCountries.sql
-- in: aLangId

with wt1 as (
  select
    country_id,
    count(*)
  from
    ref_site
  group by
    country_id
)
select 
  wt1.country_id,
  wt1.count,
  rcl.title as country,
  rcl2.title as continent 
from 
  wt1
join
  ref_country rc on
  rc.id = wt1.country_id
join
  ref_country_lang rcl on
  rcl.country_id = wt1.country_id and rcl.lang_id = {{aLangId}}
join
  ref_continent_lang rcl2 on
  rcl2.continent_id = rc.continent_id and rcl2.lang_id = {{aLangId}}
