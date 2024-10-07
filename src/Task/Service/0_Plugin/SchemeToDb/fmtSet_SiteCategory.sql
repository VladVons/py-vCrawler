-- fmtSet_SiteCategory.sql
-- in: InsValues

merge into ref_site_category as dst
using (
  values {InsValues}
) as src (enabled, site_id, path)
on (dst.site_id = src.site_id and dst.path = src.path)
when not matched then
  insert (enabled, site_id, path)
  values (src.enabled, src.site_id, src.path)
