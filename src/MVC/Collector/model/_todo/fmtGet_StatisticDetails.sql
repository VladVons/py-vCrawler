select
    rs.id,
    rs.enabled,
    rs.url,
    --count(distinct ru.*) as pages_uniq,
    (3600*24*1.5/count(ru.*))::int as sleep,
    count(ru.*) as pages_all,
    count(hu.url_id) as parsed,
    count(hu.parsed_data) as products
from
    ref_site rs
join
    ref_url ru on
    (ru.site_id = rs.id)
join
    hist_url hu on
    (hu.url_id = ru.id)
where
    (rs.enabled)
group by
    rs.id
order by
    pages_all
