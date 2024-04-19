-- Created: 2024.04.03
-- Author: Vladimir Vons <VladVons@gmail.com>
-- License: GNU, see LICENSE for more details


create type url_enum as enum (
    'none',
    'product',
    'category',
    'contact'
);


create type guard_enum as enum (
    'unknown',
    'cloudflare'
);


-- user --
create table if not exists ref_user (
    id                  serial primary key,
    create_date         timestamp default current_timestamp,
    login               varchar(16) not null unique,
    passw               varchar(34) not null,
    enabled             boolean
);

create table if not exists ref_user_ext (
    attr                varchar(32) not null,
    val                 text not null,
    enabled             boolean default true,
    user_id             int not null references ref_user(id) on delete cascade,
    unique (user_id, attr)
);


-- site --
create table if not exists ref_site (
    id                  serial primary key,
    create_date         timestamp default current_timestamp,
    unlock_date         timestamp,
    enabled             boolean,
    guard_en            guard_enum,
    url                 varchar(64) not null unique,
    update_hours        int2 not null default 72,
    urls_parse          int2 not null default 10,
    sleep_seconds       numeric(5,2) not null default 5,
    robots              text
);

create table if not exists ref_site_parser (
    create_date         timestamp default current_timestamp,
    moderated           bool default false,
    scheme              json not null,
    url_en              url_enum not null default 'product', 
    site_id             int not null references ref_site(id) on delete cascade,
    unique (site_id, url_en)
);


-- url --
create table if not exists ref_url (
    id                  serial primary key,
    create_date         timestamp default current_timestamp,
    update_date         timestamp,
    unlock_date         timestamp,
    url                 varchar(256) not null,
    url_en              url_enum,
    site_id             int not null references ref_site(id) on delete cascade,
    unique (url, site_id)
);

create table if not exists hist_url (
    id                  serial primary key,
    create_date         timestamp default current_timestamp,
    data_size           int default 0,
    url_count           smallint default 0,
    status_code         smallint,
    parsed_data         json,
    url_id              int not null references ref_url(id) on delete cascade,
    user_id             int not null references ref_user(id) on delete cascade
);
create index if not exists hist_url_idx_id on hist_url (url_id);

--

create table if not exists ref_product (
    title               varchar(128),
    category            varchar(80),
    image               varchar(128),
    sku                 varchar(24),
    mpn                 varchar(24),
    brand               varchar(24),
    price               decimal(8, 2),
    price_old           decimal(8, 2),
    stock               boolean default true,
    url_id              int not null unique references ref_url(id) on delete cascade
);
