{% extends './fmtGet_ProductsLast_.sql' %}
-- fmtGet_ProductsLastCountry.sql
-- in: aCountryId, aLimit

{% block _ref_site_join %}
  and (rs.country_id = {{aCountryId}})
{% endblock %}
