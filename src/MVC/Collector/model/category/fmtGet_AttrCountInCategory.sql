-- mtGet_AttrCountInCategory.sql
-- in: aCountryId, aCategory

select
    key,
    value,
    count(*) as count
from
    ref_product rp
join
    ref_url ru on ru.id = rp.url_id
join
  ref_site rs on rs.id = ru.site_id
cross join lateral
    jsonb_each_text(rp.attr) as data(key, value)
where
  (rs.country_id = {{aCountryId}}) and
  rp.stock and
  (key not in ('model', 'brand')) and
  (rp.attr->>'category' = '{{aCategory}}')
group by
    key, value
having
    count(*) > 5
order by
    key, value
