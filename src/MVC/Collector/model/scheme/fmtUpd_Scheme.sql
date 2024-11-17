-- fmtUpd_Scheme.sql

merge into ref_site_parser as dst
using (
  values {{aValues}}
) as src (site_id, url_en, scheme)
on 
  (dst.site_id = src.site_id) and (dst.url_en = src.url_en)
when matched then update 
  set scheme = src.scheme, update_date = now(), moderated = false
when not matched then insert 
  (site_id, url_en, scheme, update_date, moderated)
  values (src.site_id, src.url_en, src.scheme, now(), false)

