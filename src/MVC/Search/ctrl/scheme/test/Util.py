# Created: 2024.04.15
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import asyncio
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

class TCacheFileUrl(TCacheFile):
    async def Download(self, aUrl: str, aEmul: bool) -> dict:
        return await self.ProxyA(aUrl, {'emul': aEmul}, Download, [aUrl, aEmul])

Cache = TCacheFileUrl('/tmp/crawler/url', 5*60)
Cache.Clear()
