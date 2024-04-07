-- fmtGet_SiteExt.sql
-- in: aSiteId

select
    attr,
    (array_agg(val order by site_id desc))[1] as val
from
    ref_site_ext
where
    (enabled) and
    ((site_id = 0) or (site_id = {{aSiteId}}))
group by
    attr
