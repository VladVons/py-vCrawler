-- fmtGet_AliasLang.sql
-- in: aLangId

select
  --ra.title, ral.title
  jsonb_object_agg(ra.title, coalesce(ral.title, ra.title)) as lang
from
  ref_alias ra
left join ref_alias_lang ral on 
  ral.alias_id = ra.id and ral.lang_id = {{aLangId}}
