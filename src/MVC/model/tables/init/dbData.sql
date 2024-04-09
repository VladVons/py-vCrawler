INSERT INTO ref_user (id, login, passw, enabled) VALUES
     (0, 'common','none',false);

INSERT INTO ref_user_ext (attr,val,enabled,user_id) VALUES
     ('max_workers','5',true,0),
     ('speed_test_url','https://ping.virtua.cloud/100MB.bin',true,0);

