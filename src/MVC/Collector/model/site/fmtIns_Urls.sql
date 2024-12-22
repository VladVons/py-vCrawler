-- fmtIns_Url.sql
-- in: aValues(site_id, url), ...

merge into
  ref_url as dst
using (
  values {{aValues}}
) as src (site_id, url)
on (dst.url = src.url) and (dst.site_id = src.site_id)
when matched then
  do nothing
when not matched then
  insert (url, site_id)
  values (src.url, src.site_id)
