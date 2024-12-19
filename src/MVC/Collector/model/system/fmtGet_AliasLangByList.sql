-- fmtGet_AliasLangByList.sql
-- in: aLangId, aValues

select
  jsonb_object_agg(wt1.key, coalesce(ral.title, wt1.key)) AS lang
from (
  values {{aValues}}
) as wt1(key)
left join ref_alias ra on 
  ra.title = wt1.key
left join ref_alias_lang ral on 
  ral.alias_id = ra.id and ral.lang_id = {{aLangId}}
