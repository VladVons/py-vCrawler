with
wt1 as
(
  select user_id
  from hist_url
  where (create_date >= NOW() - INTERVAL '1 hour')
),
wt2 as
(
  select
    user_id,
    count(*) as cnt
  from wt1
  group by user_id
)
select
  ru.id,
  ru.login,
  ru.enabled,
  ru.note,
  wt2.cnt
from
  wt2
join
  ref_user ru on
  wt2.user_id = ru.id
order by
  cnt;


select
  count(*) cnt,
  count(distinct user_id),
  (count(*) / count(distinct user_id)) as avg
from
  hist_url
where
  (create_date >= NOW() - INTERVAL '1 hour');
