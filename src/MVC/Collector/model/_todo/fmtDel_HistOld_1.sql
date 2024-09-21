delete from hist_url
where id not in (
    select id
    from hist_url
    order by id desc
    limit 1
)
