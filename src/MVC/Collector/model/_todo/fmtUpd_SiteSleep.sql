with wt1 as (
  select
      site_id,
      round(3600*24*1.0/count(*)+5, 0) as sleep_seconds
  from
    ref_url
  group by
    site_id
  having 
    count(*) > 1
)
update ref_site
set
    sleep_seconds = wt1.sleep_seconds
from
    wt1
where
    ref_site.id = wt1.site_id and 
    ref_site.enabled
