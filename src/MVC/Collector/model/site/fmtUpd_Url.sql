-- fmtUpd_Url.sql
-- in: aUrlId, aUrlEn, aStatusCode

update ref_url
set
  update_date = now(),
  url_en = {% if aUrlEn %} '{{aUrlEn}}' {% else %} null {% endif %},
  proxy_id = {{aProxyId}},
  status_code = {{aStatusCode}}
where
  id = {{aUrlId}}
