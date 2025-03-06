{% extends './fmtGet_ProductsLast_.sql' %}
-- fmtGet_ProductsAttrSite.sql
-- in: aFilter, aPriceMin, aPriceMax, aLimit, aOffset, aSiteId

{% block _ref_site_join %}
  and (rs.id = {{aSiteId}})
{% endblock %}
