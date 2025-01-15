# Created: 2024.05.15
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


# pylint: skip-file
from Inc.DbList import TDbList
from Inc.Http.HttpUrl import UrlToDict, UrlToStr, QueryToDict
from Inc.Misc.Pagination import TPagination
from Inc.Misc.Crypt import GetCRC
from Inc.Var.Dict import DeepGetByList, GetDictDef, GetDictDefs, Filter, DelValues, GetNotNone
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

async def SeoEncodeDbl(self, aDbl: TDbList, aFields: list[str]):
    if (aDbl):
        Hrefs = []
        for xField in aFields:
            Hrefs += aDbl.ExportList(xField)

        Hrefs = await SeoEncodeList(self, Hrefs)

        Size = len(aDbl)
        for Idx, xField in enumerate(aFields):
            Offset = Idx * Size
            Part = Hrefs[Offset: Offset + Size]
            aDbl.ImportList(Part, xField)

def GetRedirectHref(aUrl: str) -> str:
    return f'href={aUrl}&chk={GetCRC(aUrl)}'

async def Img_GetCategory(self, aNames: list[str]) -> list[str]:
    Files = [f'category/{xName}.jpg' for xName in aNames]
    return await self.ExecImg(
        'system',
        {
            'method': 'GetFiles',
            'param': {
                'aFiles': Files
            }
        }
    )

async def Model_GetCategoriesCountry(self, aCountryId: int) -> dict:
    return await self.ExecModelImport(
        'category',
        {
            'method': 'GetCategoriesCountry',
            'param': {
                'aCountryId': aCountryId
            },
            'cache_age': 60*10
        }
    )
