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

vacuum full hist_url;

