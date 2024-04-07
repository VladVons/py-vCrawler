INSERT INTO ref_site (id, enabled, url) VALUES
     (0,false,'common');

INSERT INTO ref_site_ext (attr, val, site_id) VALUES
     ('update_hours','72',0),
     ('sleep_seconds','5',0),
     ('urls_parse','10',0);

INSERT INTO ref_user (id, login, passw, enabled) VALUES
     (0, 'common','none',false);

INSERT INTO ref_user_ext (attr,val,enabled,user_id) VALUES
     ('max_workers','5',true,0),
     ('speed_test_url','https://ping.virtua.cloud/100MB.bin',true,0);

