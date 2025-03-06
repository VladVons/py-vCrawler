-- fmtGet_Categories_.sql
-- in: aCountryId

select
  attr->>'category' as category,
  count(*) as count,
  min(rp.price)::int as price_min,
  max(rp.price)::int as price_max
from
  ref_product rp
join
  ref_url ru on (ru.id = rp.url_id)
join
  ref_site rs on (rs.id = ru.site_id)
  {% block _ref_site_join %}{% endblock %}
where
  (stock is true) and
  (attr->>'category' is not null)
group by
  attr->>'category'
{% block _having %}{% endblock %}
order by
  category
