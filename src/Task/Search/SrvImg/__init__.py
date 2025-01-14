# Created: 2025.01.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.SrvWeb.SrvBase import TSrvConf
from .Main import TSrvImg


def Main(aConf) -> tuple:
    SrvConf = aConf.get('srv_conf')
    Obj = TSrvImg(TSrvConf(**SrvConf))
    if (aConf.get('fs_api')):
        Res = (Obj, Obj.RunApi())
    else:
        Res = (Obj, Obj.RunApp())
    return Res
