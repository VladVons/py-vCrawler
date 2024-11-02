# Created: 2024.04.15
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import asyncio
import json
import aiohttp
from bs4 import BeautifulSoup
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

async def UrlGetData(aUrl: str) -> object:
    async def _GetUrlData(aHeaders: dict):
        async with aiohttp.ClientSession() as Session:
            try:
                async with Session.get(aUrl, headers=aHeaders) as Response:
                    Data = await Response.read()
                    Res = {'data': Data, 'status': Response.status}
            except Exception as E:
                Res = {'err': str(E), 'status': -1}
            return Res

    Headers = [
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
            'Accept-Language': 'uk'
        },
        {
            'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'Accept-Language': 'uk'
        }
    ]

    for xHeader in Headers:
        Res = await _GetUrlData(xHeader)
        if (Res['status'] not in [403, 503]):
            break
        await asyncio.sleep(1.0)
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

    def _CheckFields(aPipe: dict, aFields: list[str]) -> list:
        Res = []
        for xField in aFields:
            Val = aPipe.get(xField)
            if (Val is None):
                Res.append(f'{xField}: missed')
            else:
                if (xField in ['price', 'price_old']):
                    if (not isinstance(Val[0], (int, float))):
                        Res.append(f'{xField}: not float')
                elif (xField in ['name', 'brand', 'category', 'description']):
                    if (Val != Val.strip()):
                        Res.append(f'{xField}: not stripped')
                elif (xField == 'features'):
                    if (not isinstance(Val, dict)):
                        Res.append(f'{xField}: not key-value')
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
            Res = _CheckFields(aPipe['products'][0], Fields)
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
