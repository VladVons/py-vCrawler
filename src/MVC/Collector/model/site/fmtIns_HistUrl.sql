-- fmtIns_HistUrl.sql

insert into hist_url(
    data_size,
    url_count,
    status_code,
    parsed_data,
    crc,
    url_id,
    user_id
)
values (
    {{aDataSize}},
    {{aUrlCount}},
    {{aStatusCode}},
    {% if aParsedData %} '{{aParsedData}}' {% else %} null {% endif %},
    {{aCrc}},
    {{aUrlId}},
    {{aUserId}}
)
