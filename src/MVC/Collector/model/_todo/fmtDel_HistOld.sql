-- delete from
-- from
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

-- with wt1 as (
--     select max(id) as id, url_id 
--     from hist_url
--     group by url_id
--     having count(*) > 1
--     --order by random()
--     limit 100000
-- )
-- delete
-- from hist_url
-- where 
-- 	url_id in (select url_id from wt1) and 
-- 	id not in (select id from wt1)
 
delete from
    hist_url
where
    id not in (
      select
        max(id)
      from
        hist_url
      group by
        url_id
  );

vacuum full hist_url;

vacuum full ref_url;
vacuum full ref_product;
