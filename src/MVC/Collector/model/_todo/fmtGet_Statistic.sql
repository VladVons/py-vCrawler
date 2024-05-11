select
    rs.id,
    rs.url,
    count(distinct ru.*) as pages_uniq,
    count(ru.*) as pages_all,
    count(hu.url_id) as parsed,
    count(hu.parsed_data) as products,
    sum(hu.data_size) / 1000000 as size_m,
    round(sum(hu.data_size) / count(hu.*) / 1000000.0, 2) as page_size_m
from
    ref_site rs
left join
    ref_url ru on
    (ru.site_id = rs.id)
left join
    hist_url hu on
    (hu.url_id = ru.id)
where
    (rs.enabled)
group by
    rs.id
order by
    pages_all
