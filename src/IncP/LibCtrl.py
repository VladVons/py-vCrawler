# Created: 2024.05.15
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from base64 import b64encode
from urllib.parse import quote

# pylint: skip-file
from Inc.DbList import TDbList
from Inc.Http.HttpUrl import UrlToDict, UrlToStr, QueryToDict, QueryToStr
from Inc.Misc.Pagination import TPagination
from Inc.Misc.Crypt import GetCRC
from Inc.Var.Dict import DeepGetByList, GetDictDef, GetDictDefs, DictUpdateDef, Filter, DictFindVal, DelValues, GetNotNone
from Inc.Var.Obj import Iif, IsDigits
from IncP.CtrlBase import TCtrlBase
from .Log import Log


def DblTranslate(aDbl: TDbList, aField: str, aTrans: dict):
    aDbl.AddFieldsFill([aField + '_t'], False)
    for Rec in aDbl:
        Find = Rec.GetField(aField)
        Val = aTrans.get(Find, Find)
        aDbl.RecMerge([Val])

def GetFilterFromQuery(aQuery: dict, aPrefix: str = 'f_') -> dict:
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

async def Model_GetCategoriesSite(self, aSiteId: int) -> TDbList:
    return await self.ExecModelImport(
        'category',
        {
            'method': 'GetCategoriesSite',
            'param': {
                'aSiteId': aSiteId
            },
            'cache_age': -1
        }
    )

async def Model_GetCategoriesCountry(self, aCountryId: int) -> TDbList:
    return await self.ExecModelImport(
        'category',
        {
            'method': 'GetCategoriesCountry',
            'param': {
                'aCountryId': aCountryId
            },
            'cache_age': -1
        }
    )

async def DblGetCategories(self, aLangId: int, aId: int, aType: str) -> TDbList:
    if (aType == 'country'):
        Dbl = await Model_GetCategoriesCountry(self, aId)
        HrefFmt = '/?route=product/country&lang_id={LangId}&country_id={Id}&f_category={Category}'
    elif (aType == 'site'):
        Dbl = await Model_GetCategoriesSite(self, aId)
        HrefFmt = '/?route=product/site&lang_id={LangId}&site_id={Id}&f_category={Category}'
    else:
        raise ValueError(f'unknown type {aType}')

    Categories = Dbl.ExportList('category')
    ImageUrls = await Img_GetCategory(self, Categories)
    Translate = await self.Translate(aLangId, Categories)
    Dbl.AddFieldsFill(['lang', 'href', 'image'], False)
    for xImage, Rec in zip(ImageUrls, Dbl):
        Category = Rec.category
        Lang = Translate.get(Category, Category)
        Href = HrefFmt.format(LangId=aLangId, Id=aId, Category=Category)
        Dbl.RecMerge([Lang, Href, xImage])
    return Dbl

def DblProducts_Adjust(aDbl: TDbList, aLangId: int):
    Marker = 'findwares.com'
    Hash = quote(b64encode(Marker.encode()).decode('utf-8'))
    aDbl.AddFieldsFill(['href', 'href_int', 'href_ext', 'site'], False)
    for Rec in aDbl:
        Href = f'/?route=product/product&lang_id={aLangId}&url_id={Rec.url_id}'
        HrefInt = f'/?route=site/site&lang_id={aLangId}&site_id={Rec.site_id}'
        HrefExt = Rec.url + Iif('?' in Rec.url, '&', '?') + f'srsltid={Hash}'
        Site = UrlToDict(Rec.url)['host']
        aDbl.RecMerge([Href, HrefInt, HrefExt, Site])


def DblGetBreadcrumbs(aData: list) -> TDbList:
    return TDbList(['title', 'href'], aData)

def GetSortOrder(aSort: str) -> str:
    SortOrder = {
        'update_date': 'desc',
        'create_date': 'desc',
        'price': 'asc'
    }
    return SortOrder.get(aSort, 'asc')

def GetProductsSort(aHref: str, aCur: str) -> TDbList:
    def SortQuery(aUrlQuery: dict, aSort: str) -> dict:
        return aUrlQuery | {'sort': aSort, 'order': GetSortOrder(aSort)}

    def UrlUdate(aUrlDict: dict, aQuery: dict) -> str:
        QueryStr = QueryToStr(aQuery)
        return UrlToStr(aUrlDict | {'query': QueryStr})

    UrlDict = UrlToDict(aHref)
    UrlQuery = QueryToDict(UrlDict.get('query'))
    Dbl = TDbList().Import({
        'head': ['href', 'title', 'selected'],
        'data': [
            [f'{aHref}', 'default', ''],
            [UrlUdate(UrlDict, SortQuery(UrlQuery, 'update_date')), 'updated',  ''],
            [UrlUdate(UrlDict, SortQuery(UrlQuery, 'create_date')), 'created',  ''],
            [UrlUdate(UrlDict, SortQuery(UrlQuery, 'price')), 'price', ''],
        ]
    })

    for Rec in Dbl:
        if (aCur in Rec.href):
            Rec.SetField('selected', 'selected')
    return Dbl

