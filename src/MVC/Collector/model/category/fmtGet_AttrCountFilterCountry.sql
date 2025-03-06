{% extends './fmtGet_AttrCount_.sql' %}
-- fmtGet_AttrCountFilterCountry.sql
-- in: aAttr, aPriceMin, aPriceMax, aCountryId

{% block _ref_site_join %}
  and (rs.country_id = {{aCountryId}})
{% endblock %}

{% block _where %}
  and (rp.price between {{aPriceMin}} and {{aPriceMax}})
  and (rp.attr @> '{{aAttr}}')
{% endblock %}

{% block _having %}
having
  count(*) >= 3
{% endblock %}
