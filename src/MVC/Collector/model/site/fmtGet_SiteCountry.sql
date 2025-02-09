-- fmtGet_SiteCountry.sql
-- in: aCountryId

with wt1 as (
  select
    ru.site_id,
    count(case when ru.url_en = 'product' then 1 end) as products,
    count(case when ru.status_code != 200 then 1 end) as err,
    count(case when rp.stock then 1 end) as onstock,
    --slow! count(case when (rp.parsed_data->'price_old'->>0)::decimal > 0 then 1 end) as discount
    0 as discount
  from
    ref_url ru
  join
    ref_site rs on (rs.id = ru.site_id)
  left join
    ref_product rp on (rp.url_id = ru.id)
  where
    (rs.country_id = {{aCountryId}})
  group by
    ru.site_id
)
select
  rs.id,
  regexp_replace(rs.url, '(://[^/]+).*', '\1') as url,
  regexp_replace(rs.url, 'https?://(www\.)?([^/]+).*', '\2') as host,
  wt1.products,
  wt1.err,
  wt1.onstock,
  wt1.discount,
  (
    select count(*)
    from ref_site_category
    where (site_id = rs.id)
  ) as categories
from
  ref_site rs
left join
  wt1 on (wt1.site_id = rs.id)
where
  (rs.country_id = {{aCountryId}})
order by
  host
