-- fmtGet_HostsInUrl.sql 
-- in: aHosts ['%comp%', '%laptop%']

select
  url,
  regexp_replace(url, 'https?://(www\.)?([^/]+).*', '\2') as host
from
  ref_site
where
    url ilike any (array[{aHosts}])
