-- mtGet_AttrCountInCategoryFilter.sql
-- in: aCountryId, aFilter

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
    (rs.country_id = {{aCountryId}}) and
    (rp.stock is true) and
    (key not in ('category', 'model')) and
    (rp.attr @> '{{aFilter}}')
  group by
      key, val
  having
      count(*) > 5
)
select
  key,
  sum(cnt)::int as total,
  jsonb_object_agg(val, cnt) as stat
  --jsonb_agg(jsonb_build_object('val', val, 'cnt', cnt)) as stat
from
  wt1
group by
  key
order by
  key
