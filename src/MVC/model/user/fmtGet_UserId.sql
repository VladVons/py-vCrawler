-- fmtGet_UserId.sql
-- in: aLogin, aPassw

select
    id
from
    ref_user
where
    (enabled) and
    (login = '{{aLogin}}') and 
    (passw = '{{aPassw}}')
