-- fmtGet_SiteCategory.sql

select
  rs.url,
  array_agg(rsc.path)
from
  ref_site rs
join
  ref_site_category rsc on rsc.site_id = rs.id
group by
  rs.id
order by rs.url
