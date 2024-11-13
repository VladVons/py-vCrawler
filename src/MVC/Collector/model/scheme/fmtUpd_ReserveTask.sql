-- fmtUpd_ReserveTask.sql
-- in: aUrl, aHours

update
  ref_site
set
  unlock_date = now() + interval '{{aHours}} hours'
where
  (enabled is not true) and (url = '{{aUrl}}')
returning
  id, unlock_date
