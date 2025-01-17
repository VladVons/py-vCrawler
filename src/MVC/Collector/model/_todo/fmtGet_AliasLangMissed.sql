-- translate json field title into lowercase polish language and create SQL insertation into table ref_alias_lang

select
  ral.lang_id,
  ral.alias_id,
  ral.title
from
  ref_alias ra
left join
  ref_alias_lang ral on (ral.alias_id = ra.id) and (ral.lang_id = 2)
where
  ra.id not in (
    select alias_id
    from ref_alias_lang
    where lang_id = 3
  ) 
order by
  id
