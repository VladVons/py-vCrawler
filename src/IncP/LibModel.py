# Created: 2023.12.21
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


# pylint: skip-file
from Inc.DbList import TDbList
from Inc.Sql.DbModel import TDbModel
from Inc.Sql import DTransaction, TDbExecCursor, ListToComma, ListIntToComma, DictToComma, TDbSql
from Inc.Var.Dict import DeepGetByList, GetDictDef, GetDictDefs, DictUpdate
from Inc.Var.DictEx import DeepGetsRe
from Inc.Var.Obj import Iif
from .Log import Log


def Escape(aVal: str) -> str:
    return aVal.replace("'", "''")
