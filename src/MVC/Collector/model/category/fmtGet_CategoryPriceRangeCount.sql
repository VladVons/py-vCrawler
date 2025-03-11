-- fmtGet_CategoryPriceRangeCount.sql 
-- in: aCountryId: 1, aCategory: 'desktop', aParts: 100

with
wt_filter as (
    select
      rp.url_id,
      rp.price
    from
      ref_product rp
    join
      ref_url ru on ru.id = rp.url_id
    join
      ref_site rs on (rs.id = ru.site_id) and (rs.enabled is true) and (rs.country_id = {{aCountryId}})
    where
      (rp.stock is true) and (rp.attr->>'category' = '{{aCategory}}')
),
wt_range as (
    select
        (percentile_cont(0.005) within group (order by wf.price))::int as price_min,
        (percentile_cont(0.995) within group (order by wf.price))::int as price_max
    from wt_filter wf
)
select
    width_bucket(wf.price, wr.price_min, wr.price_max, 25) as bucket,
    max(wf.price)::int as price_top,
    count(*) as cnt
from
  wt_filter wf
join
  wt_range wr on true
group by
  bucket
order by
  bucket
