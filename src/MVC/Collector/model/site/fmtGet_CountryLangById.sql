-- fmtGet_CountryLangById.sql
-- in: aCountryId

select
  rc.id as country_id,
  rc.lang_id
from
  ref_country rc
where
  rc.id = {{aCountryId}}
