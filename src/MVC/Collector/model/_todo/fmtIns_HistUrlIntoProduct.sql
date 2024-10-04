insert into ref_product
(url_id, sku, mpn, brand, title, category, image, stock, price, price_old)
    select
        distinct on (url_id) url_id,
        (parsed_data->>'sku') as sku,
        left(parsed_data->>'mpn', 24) as mpn,
        left(parsed_data->>'brand', 24) as brand,
        left(parsed_data->>'name', 128) as title,
        left(parsed_data->>'category', 80) as category,
        left(parsed_data->>'image', 160) as image,
        coalesce((parsed_data->>'stock')::bool, false) as stock,
        (parsed_data->'price'->>0)::decimal as price,
        (parsed_data->'price_old'->>0)::decimal as price_old
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
    brand = excluded.brand,
    title = excluded.title,
    category = excluded.category,
    image = excluded.image,
    stock = excluded.stock,
    price = excluded.price,
    price_old = excluded.price_old
