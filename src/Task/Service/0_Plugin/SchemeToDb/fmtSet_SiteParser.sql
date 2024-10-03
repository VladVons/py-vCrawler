-- fmtSet_SiteParser.sql
-- in: InsValues

insert into ref_site_parser as src
  (moderated, scheme, url_en, site_id)
  values {InsValues}
on conflict (site_id, url_en) do update
set
  moderated = excluded.moderated,
  scheme = excluded.scheme
