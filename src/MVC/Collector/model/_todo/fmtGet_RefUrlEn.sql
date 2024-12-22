with wt1 as (
    select
        site_id,
        url_en,
        count(*) as url_count,
        (100.0 * count(*) / sum(count(*)) over (partition by site_id))::int  as percent
    from
        ref_url
    group by
        site_id, url_en
)
select *
from wt1
where url_en = 'category' and percent > 10
order by site_id, url_en
