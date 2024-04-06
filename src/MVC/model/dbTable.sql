-- Created: 2024.04.03
-- Author: Vladimir Vons <VladVons@gmail.com>
-- License: GNU, see LICENSE for more details


create table if not exists ref_guard (
    id                  serial primary key,
    title               varchar(16) not null unique
);

create table if not exists ref_site (
    id                  serial primary key,
    create_date         timestamp default current_timestamp,
    unlock_date         timestamp,
    update_hours        int default 72,
    sleep_seconds       numeric(3, 1) not null default 3,
    enabled             boolean,
    url                 varchar(64) not null unique,
    sitemap             varchar(32),
    guard_id            int references ref_guard(id)
);

create table if not exists ref_parser (
    site_id             int not null unique references ref_site(id),
    create_date         timestamp default current_timestamp,
    moderated           bool default false,
    scheme              json not null
);

create table if not exists ref_url (
    id                  serial primary key,
    create_date         timestamp default current_timestamp,
    update_date         timestamp,
    enabled             boolean default true,
    url                 varchar(256) not null unique,
    data_size           int default 0,
    url_count           smallint default 0,
    status_code         smallint,
    parsed_data         json,
    site_id             int not null references ref_site(id) on delete cascade
);

create table if not exists ref_url_skip (
    enabled             boolean default true,
    url                 varchar(256) not null unique,
    site_id             int not null references ref_site(id) on delete cascade
);

create table if not exists ref_user (
    id                  serial primary key,
    create_date         timestamp default current_timestamp,
    login               varchar(16) not null unique,
    passw               varchar(34) not null,
    enabled             boolean
);

create table if not exists ref_conf (
    attr                varchar(32) not null,
    val                 text,
    enabled             boolean,
    user_id             int not null references ref_user(id),
    unique (user_id, attr)
);
