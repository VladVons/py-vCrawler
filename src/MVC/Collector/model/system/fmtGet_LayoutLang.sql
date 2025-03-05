-- fmtGet_LayoutLang.sql
-- aLangId, aRoute

select
    rll.title,
    rll.descr,
    coalesce(rll.meta_title, rll.title) as meta_title,
    rll.meta_key,
    rll.meta_descr
from
    ref_layout rl
join 
    ref_layout_lang rll on
    (rll.layout_id = rl.id) and (rll.lang_id = {{aLangId}})
where
    (rl.enabled) and
    (rl.route = '{{aRoute}}')
