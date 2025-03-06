{% extends './fmtGet_Categories_.sql' %}
-- fmtGet_CategoriesSite.sql
-- in: aSiteId 

{% block _ref_site_join %}
  and (rs.id = {{aSiteId}})
{% endblock %}
