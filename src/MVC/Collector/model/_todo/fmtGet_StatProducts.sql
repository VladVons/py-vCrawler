
with wt1 as (
    select
        site_id,
        count(*) as products
    from
        ref_url
    where
      url_en = 'product'
    group by
        site_id, url_en
)
select
  rs.id,
  rs.url,
  rs.enabled,
  wt1.products
from
    ref_site rs
left join
  wt1 on wt1.site_id = rs.id
where
  rs.country_id = 2
