insert into ref_url_product
(url_id, sku, mpn, title, category, stock, price, price_old, image)
    select
        distinct on (url_id) url_id,
        (parsed_data->>'sku') as sku,
        left(parsed_data->>'mpn', 24) as mpn,
        left(parsed_data->>'name', 128) as title,
        left(parsed_data->>'category', 80) as category,
        (parsed_data->>'stock')::bool as stock,
        (parsed_data->'price'->>0)::decimal as price,
        (parsed_data->'price_old'->>0)::decimal as price_old,
        left(parsed_data->'images'->>0, 128) as image
    from
        hist_url
    where
        (parsed_data is not null)
    order by
        url_id, id desc
on conflict (url_id) do update
set
    sku = excluded.sku,
    mpn = excluded.mpn,
    title = excluded.title,
    category = excluded.category,
    stock = excluded.stock,
    price = excluded.price,
    price_old = excluded.price_old,
    image = excluded.image
