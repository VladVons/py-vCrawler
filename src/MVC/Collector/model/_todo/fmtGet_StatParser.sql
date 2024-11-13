select
  site_id,
  count(*) as product_cnt
from 
  ref_url ru 
where 
  ru.url_en = 'product' and 
  ru.site_id in (
    select
      rs.id
    from
      ref_site rs
     left join
      ref_site_parser rsp on
      rs.id = rsp.site_id
    where
      (enabled) and 
      (rsp.site_id is not null)
  )
group by 
  site_id
order by
  product_cnt
