delete from hist_url;
delete from ref_product;
delete from ref_url;

vacuum full hist_url;
vacuum full ref_product;
vacuum full ref_url;

alter sequence ref_url_id_seq restart with 1;
alter sequence hist_url_id_seq restart with 1;

insert into ref_url (site_id, url)
  select
    rs.id,
    rs.url || rsc.path as url
  from
    ref_site_category rsc
  join
    ref_site rs on rs.id = rsc.site_id
on conflict
  do nothing;

with
wt1 as (
  select rs.url || rsc.path as url
  from ref_site_category rsc
  join ref_site rs on rs.id = rsc.site_id
)
select * from wt1;
