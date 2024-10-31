-- fmtGet_SchemeRnd.sql

select
  url_en,
  scheme::text
from
  ref_site_parser
where
  site_id = (
    select id
    from ref_site
    where enabled
    order by random()
    limit 1
  )
