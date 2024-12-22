-- fmtGet_SiteInfo.sql
-- in: aLangId, aSiteId

select
  rs.id as site_id,
  rs.create_date,
  rs.url,
  rs.country_id,
  rcl.title as country_title
  from
    ref_site rs
  join
    ref_country_lang rcl on (rcl.country_id = rs.country_id) and (rcl.lang_id = {{aLangId}}) 
  where
    (rs.id = {{aSiteId}})
