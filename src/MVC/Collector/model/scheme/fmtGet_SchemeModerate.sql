-- fmtGet_SchemeModerate.sql

select
  rsp.site_id,
  rsp.url_en,
  rsp.scheme::text
from
  ref_site_parser rsp
where
    (not moderated) and
  rsp.site_id = (
    select
      site_id
    from
      ref_site_parser
    where
      (not moderated)
    order by
      moderated desc
    limit 1
  )
order by
  rsp.moderated desc
