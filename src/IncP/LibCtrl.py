# Created: 2024.05.15
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


# pylint: skip-file
from Inc.DbList import TDbList
from Inc.Misc.Pagination import TPagination
from Inc.Var.Dict import DeepGetByList, GetDictDef, GetDictDefs, Filter, DelValues
from Inc.Var.Obj import Iif, IsDigits
from .Log import Log


def DblTranslate(aDbl: TDbList, aField: str, aTrans: dict):
    aDbl.AddFieldsFill([aField + '_t'], False)
    for Rec in aDbl:
        Find = Rec.GetField(aField)
        Val = aTrans.get(Find, Find)
        aDbl.RecMerge([Val])
