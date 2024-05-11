-- fmtUpd_Url.sql
-- in: aUrlId, aUrlEn

update ref_url
set
    update_date = now(),
    url_en = {% if aUrlEn %} '{{aUrlEn}}' {% else %} null {% endif %}
where
    id = {{aUrlId}}
