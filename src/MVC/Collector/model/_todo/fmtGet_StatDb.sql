select
    (
        select pg_size_pretty(pg_database_size(datname))
        from pg_database
        where datname = 'crawler_used'
    ) as db_size,
    (
        select count(*)
        from ref_url
    ) as ref_url,
    (
        select count(update_date)
        from ref_url
    ) as ref_url_parsed,
    (
        select count(*)
        from ref_product
    ) as ref_product,
    (
        select count(*)
        from ref_product
        where stock
    ) as ref_product_stock,
    (
        select count(*)
        from hist_url
    ) as hist_url,
    (
        select pg_size_pretty(sum(data_size))
        from hist_url
        where data_size > 0
    ) as hist_size,
    (
        select pg_size_pretty(avg(data_size))
        from hist_url
        where data_size > 0
    ) as page_size,
    (
        select count(*)
        from hist_url
        where (status_code != 200)
    ) as status_err
