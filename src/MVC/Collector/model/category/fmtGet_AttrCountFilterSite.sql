{% extends './fmtGet_AttrCount_.sql' %}
-- fmtGet_AttrCountFilterSite.sql
-- in: aAttr, aPriceMin, aPriceMax, aSiteId

{% block _ref_site_join %}
  and (rs.id = {{aSiteId}})
{% endblock %}

{% block _where %}
  and (rp.price between {{aPriceMin}} and {{aPriceMax}})
  and (rp.attr @> '{{aAttr}}')
{% endblock %}
