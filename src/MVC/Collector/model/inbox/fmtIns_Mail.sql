-- fmtIns_Mail.sql

insert into doc_inbox(
  mail,
  subject,
  body,
  ip,
  inbox_en
)
values (
  '{{aMail}}',
  '{{aSubject}}',
  '{{aBody}}',
  '{{aIp}}',
  '{{aInboxEn}}'
)
returning id
