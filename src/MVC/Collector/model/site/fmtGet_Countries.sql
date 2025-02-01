-- fmtGet_Countries.sql
-- in: aLangId

select
  rc.id,
  rc.alias,
  rc.lang_id,
  count(rs.enabled) as cnt_enabled,
  rcl.title
from
  ref_site rs
join
  ref_country rc on (rc.id = rs.country_id)
join
  ref_country_lang rcl on (rcl.country_id = rs.country_id) and (rcl.lang_id = {{aLangId}})
where
  (rs.enabled is true)
group by
  rc.id,
  rcl.title
order by
  rc.alias
