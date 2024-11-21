-- fmtGet_ProductByUrlId.sq
-- in: aUrlIdl

select
        data_size,
        url_id,
        url_count,
        status_code,
        parsed_data as product,
        create_date
    from
        hist_url
    where
        url_id = {{aUrlId}}
    order by
        id desc
