-- fmtGet_UserConf.sql
-- in: aUserId

select
    attr,
    array_agg(val order by user_id desc) as val
from
    ref_conf rc
where
    rc.enabled and
    (
        (rc.user_id = 0) or
        (rc.user_id = {{aUserId}})
    )
group by
    attr
