-- fmtGet_UserExt.sql
-- in: aUserId

select
    attr,
    (array_agg(val order by user_id desc))[1] as val
from
    ref_user_ext
where
    (enabled) and
    ((user_id = 0) or (user_id = {{aUserId}}))
group by
    attr
