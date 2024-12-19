-- fmtUpd_SiteUrlToUpdateUnlock.sql
-- aSiteId, UrlIds. aLimit
-- 1.3 is extra time for 0.75 random sleep and slow emulator

with
wt1 as (
  select
    now() + ((rs.sleep_seconds * {{aLimit}} * 1.3) || ' seconds')::interval as unlock_date
  from
    ref_site rs
  where
    (rs.id = {{aSiteId}})
),
wt2 as (
  update
    ref_url
  set
    unlock_date = wt1.unlock_date
  from
    wt1
  where
    id in ({{UrlIds}})
),
wt3 as (
  update
    ref_site
  set
    unlock_date = wt1.unlock_date
  from
    wt1
  where
    id = {{aSiteId}}
)
select
