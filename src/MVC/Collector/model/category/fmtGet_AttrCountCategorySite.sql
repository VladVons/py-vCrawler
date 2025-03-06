{% extends './fmtGet_AttrCount_.sql' %}
-- fmtGet_AttrCountCategorySite.sql
-- in: aCategory, aSiteId

{% block _ref_site_join %}
  and (rs.id = {{aSiteId}})
{% endblock %}

{% block _where %}
  and (rp.attr->>'category' = '{{aCategory}}')
{% endblock %}
