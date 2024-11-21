# Created: 2024.04.15
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import json
from bs4 import BeautifulSoup
from Inc.Misc.aiohttpClient import UrlGetData
from Inc.Misc.Cache import TCacheFile
from Inc.Misc.PlayWrite import UrlGetData as PW_UrlGetData
from Inc.Scheme.Scheme import TSchemeExt, TSchemeApi
from Inc.Util.ModHelp import GetClass
from Inc.Var.Obj import GetTree


async def Download(aUrl: str, aEmul: bool) -> dict:
    if (aEmul):
        Res = await PW_UrlGetData(aUrl)
    else:
        Res = await UrlGetData(aUrl)
    return Res

def GetSoup(aData: str) -> BeautifulSoup:
    Res = BeautifulSoup(aData, 'lxml')
    if (len(Res) == 0):
        Res = BeautifulSoup(aData, 'html.parser')
    return Res


def LoadScript(aScript: str) -> dict:
    try:
        Res = json.loads(aScript)
    except Exception as E:
        Res = {'err': f'json: {E}'}
    return Res

def GetMacroses(aScheme: dict) -> dict:
    Res = {}
    BS4 = ['find', 'find_all', 'text', 'get']
    Methods = GetClass(TSchemeApi) + GetClass(TSchemeExt)
    Methods = [xMethod[0] for xMethod in Methods] + BS4
    for _Nested, _Path, Obj, _Depth in GetTree(aScheme):
        if (isinstance(Obj, list)) and (len(Obj) > 0):
            Method = Obj[0]
            if (isinstance(Method, str)) and (Method in Methods):
                if (Method not in Res):
                    Res[Method] = 0
                Res[Method] += 1
    return Res

def CheckPipe(aPipe: dict, aType: str) -> list:
    def _CheckUrlPrefix(aUrls: list[str]) -> list:
        return [
            f'missed http in url: {xUrl}'
            for xUrl in aUrls
            if (isinstance(xUrl, str)) and (not xUrl.startswith('http'))
        ]

    def _CheckType(aField: str, aVal: object) -> str:
        if (aField in ['price', 'price_old', 'images']):
            if (not isinstance(aVal, list)):
                return f'{aField}: must be list'

            if (aField in ['price', 'price_old']):
                if (not isinstance(aVal[0], (int, float))):
                    return f'{aField}: {aVal[0]} must be digit'

                if (not aVal[1]):
                    return f'{aField}: currency is empty'
        elif (aField in ['name', 'brand', 'image', 'category', 'description', 'href']):
            if (not isinstance(aVal, str)):
                return f'{aField}: must be string'
        elif (aField == 'features'):
            if (not isinstance(aVal, dict)):
                return f'{aField}: must be dict'
        elif (aField == 'stock'):
            if (not isinstance(aVal, bool)):
                return f'{aField}: must be logical'

    def _CheckFields(aPipe: dict, aFields: list[str]) -> list:
        cMinLen = {
            'description': 120
        }

        Res = []
        for xField in aFields:
            Val = aPipe.get(xField)
            if (Val is None):
                Res.append(f'{xField}: missed')
                continue

            R = _CheckType(xField, Val)
            if (R):
                Res.append(R)
                continue

            if (xField in ['name', 'brand', 'category', 'description', 'href', 'image']):
                if (Val != Val.strip()):
                    Res.append(f'{xField}: not stripped')

                MinLen = cMinLen.get(xField)
                if (MinLen and len(Val) < MinLen):
                    Res.append(f'{xField}: too short')
        return Res

    Urls = []
    if (aType == 'product'):
        Fields = ['name', 'brand', 'image', 'images', 'stock', 'price', 'price_old', 'category', 'features', 'description']
        if (isinstance(aPipe.get('images'), list)):
            Urls += aPipe['images']
        if (isinstance(aPipe.get('image'), str)):
            Urls += [aPipe['image']]
        Res = _CheckFields(aPipe, Fields) + _CheckUrlPrefix(Urls)
    elif (aType == 'category'):
        Fields = ['products', 'pager']
        Res = _CheckFields(aPipe, Fields)
        if (isinstance(aPipe.get('products'), list)):
            Urls += [x.get('href') for x in aPipe['products']]
            Fields = ['href', 'name', 'stock', 'price']
            Products = aPipe['products']
            if (Products):
                Res = _CheckFields(Products[0], Fields)
            else:
                Res = ['no products']
        if (isinstance(aPipe.get('pipe'), list)):
            Urls += aPipe['pager']
        Res += _CheckUrlPrefix(Urls)
    else:
        Fields = []
    return Res


class TCacheFileUrl(TCacheFile):
    def _SetBefore(self, _aPath: str, aData: object):
        if (aData['status'] == 200):
            return aData

    async def Download(self, aUrl: str, aEmul: bool) -> dict:
        return await self.ProxyA(aUrl, {'emul': aEmul}, Download, [aUrl, aEmul])


Cache = TCacheFileUrl('/tmp/crawler/cache', 5*60)
Cache.Clear()
