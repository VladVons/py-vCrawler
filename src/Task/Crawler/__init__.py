# Created: 2024.04.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.SrvWeb.SrvBase import TSrvConf
from .Api import ApiCtrls
from .Main import TSrvCtrl


def Main(aConf) -> tuple:
    SrvConf = aConf.get('srv_conf')
    Obj = TSrvCtrl(TSrvConf(**SrvConf))
    if (aConf.get('fs_api')):
        Res = (Obj, Obj.RunApi())
    else:
        Res = (Obj, Obj.RunApp())
    return Res
