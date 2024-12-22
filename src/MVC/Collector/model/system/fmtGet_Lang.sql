-- fmtGet_Lang.sql
-- in: aLangId

select
  rl.id,
  rl.alias,
  rll.title
from
  ref_lang rl
left join
  ref_lang_lang rll on (rll.lang_id2 = rl.id) and (rll.lang_id = {{aLangId}})
where
  (rl.enabled is true)
