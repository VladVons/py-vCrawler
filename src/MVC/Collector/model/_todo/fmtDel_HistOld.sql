-- delete from
--     hist_url
-- where
--     id not in (
--       select
--         max(id)
--       from
--         hist_url
--       group by
--         url_id
--   );

-- speed too
--delete from hist_url hu
--where exists (
--    select 1
--    from (
--        select max(id) as id, url_id
--        from hist_url
--        group by url_id
--        having count(*) > 1
--    ) wt1
--    where hu.url_id = wt1.url_id
--    and hu.id <> wt1.id
--);

with wt1 as (
  select max(id) as id, url_id
  from hist_url
  group by url_id
  having count(*) > 1
  limit 100000
)
delete
from hist_url hu
using wt1
where
  (hu.url_id = wt1.url_id) and
  (hu.id <> wt1.id);

analyze hist_url;
vacuum full hist_url;
vacuum full ref_url;
vacuum full ref_product;
