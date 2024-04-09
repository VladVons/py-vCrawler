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

create or replace trigger ref_site_taiu
    after insert on ref_site
    for each row
    execute function ref_site_fai();
