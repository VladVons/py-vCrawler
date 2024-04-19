-- Created: 2024.04.06
-- Author: Vladimir Vons <VladVons@gmail.com>
-- License: GNU, see LICENSE for more details


create or replace function ref_site_fai() returns trigger
as $$
begin
    insert into ref_url (site_id, url)
    values (new.id, new.url);
    return new;
end $$ language plpgsql;

create or replace trigger ref_site_tai
    after insert on ref_site
    for each row
    execute function ref_site_fai();

--

create or replace function hist_url_fai() returns trigger
as $$
begin
    insert into ref_product
        (url_id, sku, mpn, brand, title, category, image, stock, price, price_old)
    values (
        new.url_id,
        new.parsed_data->>'sku',
        left(new.parsed_data->>'mpn', 24),
        left(new.parsed_data->>'brand', 24),
        left(new.parsed_data->>'name', 128),
        left(new.parsed_data->>'category', 80),
        left(new.parsed_data->'images'->>0, 128),
        (new.parsed_data->>'stock')::bool,
        (new.parsed_data->'price'->>0)::decimal,
        (new.parsed_data->'price_old'->>0)::decimal
    )
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
        price_old = excluded.price_old;
    return new;
end $$ language plpgsql;

create or replace trigger hist_url_tai
    after insert on hist_url
    for each row
    execute function hist_url_fai();

--
