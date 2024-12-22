-- fmtGet_SchemeRnd.sql

select
  site_id,
  url_en,
  scheme::text
from
  ref_site_parser
where
  site_id = (
    select id
    from ref_site
    where (enabled is true)
    order by random()
    limit 1
  )
