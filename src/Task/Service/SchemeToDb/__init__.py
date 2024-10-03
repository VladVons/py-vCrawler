# Created: 2024.10.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from .Main import TMain


def Main(_aConf) -> tuple:
    Obj = TMain()
    return (Obj, Obj.Run())
