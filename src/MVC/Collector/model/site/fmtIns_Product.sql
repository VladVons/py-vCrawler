-- fmtIns_Product.sql
-- in: aUrlId, aParsedData, aAttr, aTitle, aStock, aPrice

insert into ref_product
(
  update_date,
  url_id,
  title,
  stock,
  price,
  parsed_data,
  attr,
  crc
)
values
(
  now(),
  {{aUrlId}},
  '{{aTitle}}',
  {{aStock}},
  {{aPrice}},
  {% if aParsedData %} '{{aParsedData}}' {% else %} null {% endif %},
  {% if aAttr %} '{{aAttr}}' {% else %} null {% endif %},
  {{aCrc}}
)
on conflict (url_id) do update
set
  update_date = excluded.update_date,
  title = excluded.title,
  stock = excluded.stock,
  price = excluded.price,
  parsed_data = excluded.parsed_data,
  attr = excluded.attr,
  crc = excluded.crc
