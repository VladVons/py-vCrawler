-- Created: 2024.04.03
-- Author: Vladimir Vons <VladVons@gmail.com>
-- License: GNU, see LICENSE for more details


create type url_enum as enum (
    'product',
    'category',
    'contact'
);


-- site --
create table if not exists ref_site (
    id                  serial primary key,
    create_date         timestamp default current_timestamp,
    unlock_date         timestamp,
    enabled             boolean,
    url                 varchar(64) not null unique
);

create table if not exists ref_site_ext (
    attr                varchar(32) not null,
    val                 text not null,
    enabled             boolean default true,
    site_id             int not null references ref_site(id) on delete cascade,
    unique (site_id, attr)
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
    url                 varchar(256) not null unique,
    url_en              url_enum default 'product',
    site_id             int not null references ref_site(id) on delete cascade
);

create table if not exists hist_url (
    id                  serial primary key,
    create_date         timestamp default current_timestamp,
    data_size           int default 0,
    url_count           smallint default 0,
    status_code         smallint,
    parsed_data         json,
    url_id              int not null references ref_url(id) on delete cascade
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
