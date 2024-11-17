-- fmtGet_Countries.sql

select
  rc.id,
  rc.alias
from
  ref_site rs
join
  ref_country rc on
  rc.id = rs.country_id
group by
  rc.id
order by
  rc.alias
