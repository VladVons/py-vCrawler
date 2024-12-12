-- fmtGet_CountryCategories.sql
-- in: aCountryId

select
  attr->>'category' as category,
  count(*) as count
from
  ref_product rp
join
  ref_url ru on ru.id = rp.url_id
join
  ref_site rs on rs.id = ru.site_id and rs.country_id = {{aCountryId}}
where
  stock and
  (attr->>'category' is not null)
group by
  attr->>'category'
having
  count(*) >= 5
order by
  category
