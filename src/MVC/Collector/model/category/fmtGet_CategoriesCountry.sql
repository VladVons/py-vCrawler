{% extends './fmtGet_Categories_.sql' %}
-- fmtGet_CategoriesCountry.sql
-- in: aCountryId 

{% block _ref_site_join %}
  and (rs.country_id = {{aCountryId}})
{% endblock %}

{% block _having %}
having
  count(*) >= 3
{% endblock %}
