-- fmtSet_Site.sql
-- in: InsValues, SelValues

merge into ref_site as dst
using (
  values {InsValues}
) as src (url, country_id)
on (dst.url = src.url)
when matched then
  do nothing
when not matched then
  insert (url, country_id)
  values (src.url, src.country_id)
;

select id, url
from ref_site
where url in ({SelValues})
;
