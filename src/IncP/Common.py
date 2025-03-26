# Created: 2025.01.29
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


# pylint: skip-file
from Inc.Var.Dict import DictToPath

gImgProxy = 'img-pxy'

def AdjustAttr(aAttr: dict) -> dict:
    if (aAttr):
        Res = DictToPath(aAttr)
        for xKey in list(Res.keys()):
            xVal = Res[xKey]
            if (isinstance(xVal, str)):
                Res[xKey] = xVal.lower()

            if (xKey in ['cpu/gen', 'ram/unit', 'storage/unit']):
                del Res[xKey]
    else:
        Res = {}
    return Res
