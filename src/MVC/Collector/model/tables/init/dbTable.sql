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

-- lang

create table if not exists ref_lang (
    id              smallserial primary key,
    enabled         boolean default true,
    alias           varchar(2) not null unique
);

create table if not exists ref_lang_lang (
    id              smallserial primary key,
    title           varchar(16) not null,
    lang_id         smallint not null references ref_lang(id)
);

-- continent --

create table ref_continent (
    id              smallserial primary key,
    alias           varchar(2) not null unique
);

create table ref_continent_lang (
    id              smallserial primary key,
    title           varchar(16) not null,
    continent_id    smallint not null references ref_continent(id) on delete cascade,
    lang_id         smallint not null references ref_lang(id),
    unique(continent_id, lang_id)
);

-- country

create table ref_country (
    id              smallserial primary key,
    alias           varchar(2) not null unique,
    population      int,
    continent_id    smallint not null references ref_continent(id)
);

create table ref_country_lang (
    id              smallserial primary key,
    title           varchar(16) not null,
    country_id      smallint not null references ref_country(id) on delete cascade,
    lang_id         smallint not null references ref_lang(id),
    unique(country_id, lang_id)
);

-- user --

create table if not exists ref_user (
    id                  serial primary key,
    create_date         timestamp default current_timestamp,
    login               varchar(16) not null unique,
    passw               varchar(34) not null,
    enabled             boolean,
    note                varchar(16)
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
    update_hours        int2 not null default 12,
    urls_parse          int2 not null default 5,
    sleep_seconds       numeric(6,1) not null default 15,
    robots              text,
    headers             json,
    country_zone        varchar(8),
    note                varchar(16),
    country_id          smallint not null references ref_country(id)
);

create table if not exists ref_site_parser (
    create_date         timestamp default current_timestamp,
    update_date         timestamp,
    moderated           bool default false,
    scheme              json not null,
    url_en              url_enum not null default 'product', 
    site_id             int not null references ref_site(id) on delete cascade,
    unique (site_id, url_en)
);

create table if not exists ref_site_category (
    id                  serial primary key,
    create_date         timestamp default current_timestamp,
    enabled             boolean default true,
    path                varchar(128) not null,
    site_id             int not null references ref_site(id) on delete cascade,
    unique (site_id, path)
);


-- url --
create table if not exists ref_url (
    id                  serial primary key,
    create_date         timestamp default current_timestamp,
    update_date         timestamp,
    unlock_date         timestamp,
    url                 varchar(256) not null,
    url_en              url_enum,
    status_code         smallint,
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
    update_date         timestamp,
    title               varchar(128),
    category            varchar(80),
    image               varchar(256),
    sku                 varchar(24),
    mpn                 varchar(24),
    brand               varchar(24),
    price               decimal(8, 2),
    price_old           decimal(8, 2),
    stock               boolean default true,
    tsv_title           tsvector generated always as (to_tsvector('russian', regexp_replace(title, '[-/]', ' ', 'g'))) stored,
    url_id              int not null unique references ref_url(id) on delete cascade
);
alter table ref_product add column tsv_title tsvector generated always as (to_tsvector('simple', regexp_replace(title, '[-/]', ' ', 'g'))) stored;
create index ref_product_tvs_idx on ref_product using gin (tsv_title);

