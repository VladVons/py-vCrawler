# Created: 2024.05.07
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Task import ConfTask
from .Main import TSrvView, TSrvViewConf


def Main(aConf) -> tuple:
    Conf = aConf.get('srv_conf', {})
    SrvViewFormConf = TSrvViewConf(**Conf)
    Obj = TSrvView(SrvViewFormConf)
    return (Obj, Obj.RunApp())
