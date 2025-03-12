select
    hs.ip,
    date_trunc('second', hpv.create_date) as access_second,
    count(*) as access_count
from
  hist_session hs
left join
  hist_page_view hpv on (hpv.session_id = hs.id)
where
  (hpv.create_date >= now() - interval '7 days')
group by
  hs.ip,
  access_second
having
  count(*) >= 2
order by
  access_count desc
