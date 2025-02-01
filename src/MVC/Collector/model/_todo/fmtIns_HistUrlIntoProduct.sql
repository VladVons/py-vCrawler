-- fmtIns_HistUrlIntoProduct.sql

insert into ref_product
(url_id, title, stock, price)
    select
        distinct on (url_id) url_id,
        left(parsed_data->>'name', 128) as title,
        coalesce((parsed_data->>'stock')::bool, false) as stock,
        (parsed_data->'price'->>0)::decimal as price
    from
        hist_url
    where
        (parsed_data is not null)
    order by
        url_id,
        id desc
on conflict (url_id) do update
set
    title = excluded.title,
    stock = excluded.stock,
    price = excluded.price
