-- fmtGet_SchemeNew.sql

select
  id as site_id,
  url
from
  ref_site rs
 left join
  ref_site_parser rsp on
  rs.id = rsp.site_id
where
  ((rs.unlock_date is null) or (rs.unlock_date < now())) and
  (rsp.site_id is null)
order by
  random()
limit
  1
