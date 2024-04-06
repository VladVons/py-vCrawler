# Created: 2024.04.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.SrvWeb.SrvBase import TSrvConf
from .Main import TCrawler


def Main(aConf) -> tuple:
    SrvConf = aConf.get('srv_conf')
    Obj = TCrawler(TSrvConf(**SrvConf))
    if (aConf.get('fs_api')):
        Res = (Obj, Obj.RunApi())
    else:
        Res = (Obj, Obj.RunApp())
    return Res
