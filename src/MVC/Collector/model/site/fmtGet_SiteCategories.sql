-- fmtGet_SiteCategories.sql
-- in: aSiteId

select
  val as category,
  count(*) as cnt
from
  ref_product rp
join
  ref_url ru on ru.id = rp.url_id
join
  ref_site rs on rs.id = ru.site_id
cross join lateral
  jsonb_each_text(rp.attr) as data(key, val)
where
  (rs.id = {{aSiteId}}) and
  (rp.stock is true) and
  (key = 'category')
group by
  key, val
