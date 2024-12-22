-- fmtGet_CountryCategoriesSite.sql
-- in: aSiteId

select
  attr->>'category' as category,
  count(*) as count
from
  ref_product rp
join
  ref_url ru on (ru.id = rp.url_id)
join
  ref_site rs on (rs.id = ru.site_id) and (rs.id = {{aSiteId}})
where
  (stock is true) and
  (attr->>'category' is not null)
group by
  attr->>'category'
order by
  category
