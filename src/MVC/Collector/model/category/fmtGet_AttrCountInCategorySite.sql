-- fmtGet_AttrCountInCategorySite.sql
-- in: aSiteId, aCategory

with
wt1 as (
  select
      key,
      val,
      count(*) as cnt
  from
      ref_product rp
  join
      ref_url ru on (ru.id = rp.url_id)
  join
    ref_site rs on (rs.id = ru.site_id)
  cross join lateral
      jsonb_each_text(rp.attr) as data(key, val)
  where
    (rs.id = {{aSiteId}}) and
    (rp.stock is true) and
    (key not in ('category', 'model')) and
    (rp.attr->>'category' = '{{aCategory}}')
  group by
      key, val
)
select
  key,
  jsonb_agg(jsonb_build_object('val', val, 'cnt', cnt)) as stat
from
  wt1
group by
  key
order by
  key
