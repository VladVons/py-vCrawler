select 
  ru.site_id,
  rs.sleep_seconds,
  to_char(ru.unlock_date, 'YYYY-MM-DD HH24:MI:SS') as unlock_date,
  ru.url
from 
  ref_url ru
join 
  ref_site rs on
  (rs.id = ru.site_id)
where 
  (ru.unlock_date >= now())  
order by 
  url;

select 
  rs.id,
  rs.sleep_seconds,
  to_char(rs.unlock_date, 'YYYY-MM-DD HH24:MI:SS') as unlock_date,
  rs.url
from 
  ref_site rs
where 
  (rs.unlock_date >= now())  
order by 
  url;

select 
  rs.id,
  rs.sleep_seconds,
  to_char(rs.unlock_date, 'YYYY-MM-DD HH24:MI:SS') as unlock_date,
  rs.url
from 
  ref_site rs
where 
  id not in (
    select id
    from ref_site
    where (unlock_date >= now())  
  )
order by 
  url;
