# Created: 2025.04.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.SrvWeb import TSrvConf
from .Main import TSrvChat


def Main(aConf) -> tuple:
    Conf = aConf.get('srv_conf', {})
    SrvConf = TSrvConf(**Conf)
    Obj = TSrvChat(SrvConf)
    return (Obj, Obj.RunApp())
