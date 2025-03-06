{% extends './fmtGet_AttrCount_.sql' %}
-- fmtGet_AttrCountCategoryCountry.sql
-- in: aCategory, aCountryId

{% block _ref_site_join %}
  and (rs.country_id = {{aCountryId}})
{% endblock %}

{% block _where %}
  and (rp.attr->>'category' = '{{aCategory}}')
{% endblock %}

{% block _having %}
having
  count(*) >= 3
{% endblock %}
