select
    *
from
    hist_url
where
    (id) not in (
    select
        max(id)
    from
        hist_url
    group by
        url_id
)
order by
    url_id,
    id
