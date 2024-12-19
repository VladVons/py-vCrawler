-- fmtGet_Countries.sql

select
  rc.id,
  rc.alias,
  rc.lang_id,
  count(rs.enabled) as cnt_enabled
from
  ref_site rs
join
  ref_country rc on
  rc.id = rs.country_id
group by
  rc.id
order by
  rc.alias
