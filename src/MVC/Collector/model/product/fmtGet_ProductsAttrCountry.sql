{% extends './fmtGet_ProductsLast_.sql' %}
-- fmtGet_ProductsAttrCountry.sql
-- in: aFilter, aPriceMin, aPriceMax, aLimit, aOffset, aCountryId

{% block _ref_site_join %}
  and (rs.country_id = {{aCountryId}})
{% endblock %}
