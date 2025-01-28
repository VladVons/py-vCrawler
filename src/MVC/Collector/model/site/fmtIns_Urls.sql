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
  values (src.url, src.site_id);

-- result
select
  ru.id,
  ru.url,
  rp.crc
from
  ref_url ru
left join ref_product rp
  on rp.url_id = ru.id
where
  (site_id, url) in ({{aValues}});
