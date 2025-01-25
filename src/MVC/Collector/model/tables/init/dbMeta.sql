-- Created: 2024.04.06
-- Author: Vladimir Vons <VladVons@gmail.com>
-- License: GNU, see LICENSE for more details


--create or replace function ref_site_fai() returns trigger
--as $$
--begin
--    insert into ref_url (site_id, url)
--    values (new.id, new.url)
--    on conflict (url, site_id) do nothing;
--
--    return new;
--end $$ language plpgsql;

--create or replace trigger ref_site_tai
--    after insert on ref_site
--    for each row
--    execute function ref_site_fai();

--

create or replace function ref_site_category_fai() returns trigger
as $$
begin
    insert into ref_url (site_id, url)
    select rs.id, rs.url || new.path
    from ref_site rs
    where rs.id = new.site_id
    on conflict (url, site_id) do nothing;

    return new;
end $$ language plpgsql;

create or replace trigger ref_site_category_tai
    after insert on ref_site_category
    for each row
    execute function ref_site_category_fai();

--

create or replace function hist_url_fai() returns trigger
as $$
begin
    insert into ref_product
        (update_date, url_id, sku, mpn, brand, title, category, image, stock, price, price_old)
    values (
        now(),
        new.url_id,
        new.parsed_data->>'sku',
        left(new.parsed_data->>'mpn', 24),
        left(new.parsed_data->>'brand', 24),
        left(new.parsed_data->>'name', 128),
        left(new.parsed_data->>'category', 80),
        left(new.parsed_data->>'image', 256),
        coalesce((new.parsed_data->>'stock')::bool, false),
        (new.parsed_data->'price'->>0)::decimal,
        (new.parsed_data->'price_old'->>0)::decimal
    )
    on conflict (url_id) do update
    set
        update_date = now(),
        sku = excluded.sku,
        mpn = excluded.mpn,
        brand = excluded.brand,
        title = excluded.title,
        category = excluded.category,
        image = excluded.image,
        stock = (excluded.stock = true),
        price = excluded.price,
        price_old = excluded.price_old;
    return new;
end $$ language plpgsql;

create or replace trigger hist_url_tai
    after insert on hist_url
    for each row
    when (new.parsed_data is not null)
    execute function hist_url_fai();

---

create or replace function ref_url_fau() returns trigger 
as $$
begin
  delete from ref_product
  where url_id = new.id;

  return new;
end $$ language plpgsql;

create or replace trigger ref_url_tau
  after update of url_en, status_code on ref_url
  for each row
  when (new.url_en is null or new.url_en != 'product' or new.status_code != 200)
  execute function ref_url_fau();
