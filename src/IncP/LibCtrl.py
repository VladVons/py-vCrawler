# Created: 2024.05.15
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


# pylint: skip-file
from Inc.DbList import TDbList
from Inc.Http.HttpUrl import UrlToDict
from Inc.Misc.Pagination import TPagination
from Inc.Var.Dict import DeepGetByList, GetDictDef, GetDictDefs, Filter, DelValues
from Inc.Var.Obj import Iif, IsDigits
from IncP.CtrlBase import TCtrlBase
from .Log import Log


def DblTranslate(aDbl: TDbList, aField: str, aTrans: dict):
    aDbl.AddFieldsFill([aField + '_t'], False)
    for Rec in aDbl:
        Find = Rec.GetField(aField)
        Val = aTrans.get(Find, Find)
        aDbl.RecMerge([Val])

def GetFilterFromQuery(aQuery: dict, aPrefix: str = 'f_'):
    Res = {}
    for xKey, xVal in aQuery.items():
        if (xKey.startswith(aPrefix)):
            Key = xKey.replace(aPrefix, '')
            Res[Key] = int(xVal) if ('size' in Key and xVal) else xVal
    return Res

def ResGetItem(aData: dict, aName: str) -> str:
    return aData['res'].get(aName, '')

def ResLang(aData: dict, aName: str, aDef = None) -> str:
    Res = DeepGetByList(aData, ['res', 'lang', aName])
    if (Res is None):
        Res = Iif(aDef is None, aName, aDef)
    return Res

async def SeoEncodeList(self, aPaths: list[str]) -> list[str]:
    if (aPaths):
        return await self.ApiCtrl.Exec(
            'seo',
            {
                'type': 'api',
                'method': 'Encode',
                'param': {
                    'aPath': aPaths
                }
            }
        )

async def SeoEncodeDbl(self, aDbl: TDbList, aField: str):
    Hrefs = aDbl.ExportList(aField)
    Hrefs = await SeoEncodeList(self, Hrefs)
    aDbl.ImportList(Hrefs, aField)

async def SeoEncodeDict(self, aHref: dict) -> dict:
    Res = await SeoEncodeList(self, aHref.values())
    return dict(zip(aHref.keys(), Res))

async def SeoEncodeStr(self, aHref: str) -> str:
    Res = await SeoEncodeList(self, [aHref])
    return Res[0]
