-- fmtGet_Categories_.sql
-- in: aCountryId

select
  rp.attr->>'category' as category,
  count(*) as count,
  min(rp.price)::int as price_min,
  max(rp.price)::int as price_max,
  (percentile_cont(0.01) within group (order by rp.price))::int as price_min_pct,
  (percentile_cont(0.99) within group (order by rp.price))::int as price_max_pct
from
  ref_product rp
join
  ref_url ru on (ru.id = rp.url_id)
join
  ref_site rs on (rs.id = ru.site_id) and (rs.enabled is true)
  {% block _ref_site_join %}{% endblock %}
where
  (rp.stock is true) and
  (rp.attr->>'category' is not null)
group by
  rp.attr->>'category'
{% block _having %}{% endblock %}
order by
  category
