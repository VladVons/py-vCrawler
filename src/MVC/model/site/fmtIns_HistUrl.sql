-- fmtIns_HistUrl.sql

insert into hist_url(
    data_size,
    url_count,
    status_code,
    parsed_data,
    url_id,
    user_id
)
values (
    {{aDataSize}},
    {{aUrlCount}},
    {{aStatusCode}},
    {% if aParsedData %} '{{aParsedData}}' {% else %} null {% endif %},
    {{aUrlId}},
    {{aUserId}}
)
