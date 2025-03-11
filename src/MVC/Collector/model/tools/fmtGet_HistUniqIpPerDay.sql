-- fmtGet_HistUniqIpPerDay.sql
-- in: aHost, aLimit, aOffset

select
    count(*) over() as total,
    count(*),
    --extract(dow from hpv.create_date::date)+1 as dow,
    TO_CHAR(hpv.create_date::date, 'Day') AS dow,
    hpv.create_date::date::varchar as create_day,
    count(distinct hs.ip) as count_ip,
    count(distinct hs.id) as count_id,
    count(distinct hs.location) as count_location,
    count(distinct hpv.url) as count_url
from
    hist_page_view hpv
left join
    hist_session hs on
    (hs.id = hpv.session_id)
where
    --(hpv.url ~'route=') and
    (hs.uagent !~*'(bot|facebook)') and
    (hs.location ilike '%ukraine%') and
    (hs.ip  !~'127.0.0.1|5.58.222.201|5.58.78.170|46.173.175.188')
group by
    hpv.create_date::date
order by
    create_day desc
limit
    {{aLimit}}
offset
    {{aOffset}}
