-- fmtGet_SchemeNew.sql

select
  url
from 
  ref_site rs
 left join
  ref_site_parser rsp on
  rs.id = rsp.site_id
where
  (rs.unlock_date is null) and
  (rsp.site_id is null)
order by
  random()
limit
  1
