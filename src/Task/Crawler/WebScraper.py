# Created: 2024.04.08
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import random
import asyncio
from urllib.parse import urlparse
import aiohttp
from bs4 import BeautifulSoup
from protego import Protego
#
from Inc.Scheme.Scheme import TScheme
from Inc.Util.Str import StartsWith
from Inc.Util.Obj import GetTree
from .Api import TApiCrawlerEx


def GetSoup(aData: str) -> BeautifulSoup:
    Res = BeautifulSoup(aData, 'lxml')
    if (len(Res) == 0):
        Res = BeautifulSoup(aData, 'html.parser')
    return Res

def IsMimeApp(aUrl: str) -> bool:
    Path = urlparse(aUrl).path
    Ext = os.path.splitext(Path)[1].lower()
    if (Ext == '' or Ext in ['.php']):
        Res = False
    else:
        Mime = [
            '.zip', '.rar', '.7z', '.gz', '.bz',
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.ico',
            '.wav', '.mp3', '.mp4', '.mpeg',
            '.xml', '.pdf', '.doc', '.docx', '.xls', '.xlsx'
        ]
        Res = (Ext in Mime)
    return Res

async def GetUrlData(aUrl: str) -> object:
    Headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
    }

    async with aiohttp.ClientSession() as Session:
        try:
            async with Session.get(aUrl, headers=Headers) as Response:
                Data = await Response.read()
                Res = {'data': Data, 'status': Response.status}
        except Exception as E:
            Res = {'err': str(E)}
        return Res

async def InitRobots(aUrl: str) -> Protego:
    UrlData = await GetUrlData(aUrl)
    Content = ''
    if (UrlData['status'] == 200):
        Content = UrlData['data'].decode()
    return Protego.parse(content=Content)

def EscForSQL(aData: dict):
    for _Nested, _Path, Obj, _Depth in GetTree(aData):
        if (isinstance(Obj, dict)):
            for Key in Obj:
                if (isinstance(Obj[Key], str)) and ("'" in Obj[Key]):
                    Obj[Key] = Obj[Key].replace("'", "''")


class TWebScraper():
    def __init__(self, aApi: TApiCrawlerEx, aData: dict):
        self.Api = aApi
        self.DblSite = aData['site']
        self.DblUrl = aData['url']
        self.UrlRoot = self.DblSite.Rec.url
        self.Scheme = TScheme(self.DblSite.Rec.scheme)
        self.Robots: Protego

    def GetHrefs(self, aSoup) -> set:
        Res = set()
        for xUrl in aSoup.find_all('a'):
            xUrl = xUrl.get('href', '').strip().rstrip('/')
            if (not xUrl) or \
               (StartsWith(xUrl, ['#', 'javascript:', 'tel:', 'mailto:', 'viber:', 'tg:'])) or \
               ((xUrl.startswith('http')) and (not xUrl.startswith(self.UrlRoot))) or \
               (IsMimeApp(xUrl)) or \
               (not self.Robots.can_fetch(xUrl, '*')):
                continue

            xUrl = xUrl.rsplit('#', maxsplit=1)[0]
            if (xUrl.startswith('/')):
                xUrl = self.UrlRoot + xUrl
            Res.add(xUrl)
        return Res

    async def Exec(self) -> dict:
        self.Robots = await InitRobots(f'{self.UrlRoot}/robots.txt')

        TotalProduct = 0
        TotalDataSize = 0
        TotalHref = set()
        for Rec in self.DblUrl:
            ParsedData = None
            UrlCount = 0
            DataSize = 0

            # Data = await GetUrlData('http://oster.com.ua/c600320/p647163.html')
            # with open('debug.html', 'wb') as F:
            #     F.write(Data['data'])

            Data = await GetUrlData(Rec.url)
            if (Data['status'] == 200):
                DataSize = len(Data['data'])
                TotalDataSize += DataSize

                Soup = GetSoup(Data['data'])
                Htrefs = self.GetHrefs(Soup)
                if (Htrefs):
                    UrlCount = len(Htrefs)
                    Diff = Htrefs - TotalHref
                    if (Diff):
                        TotalHref.update(Diff)
                        await self.Api.ExecModel(
                            'ctrl',
                            {
                                'method': 'InsUrls',
                                'param': {
                                    'aSiteId': self.DblSite.Rec.id,
                                    'aUrls': list(Diff)
                                }
                            }
                        )
                self.Scheme.Parse(Soup)
                Price = self.Scheme.Pipe.get('product.pipe.price')
                if (self.Scheme.Pipe.get('product.pipe.name')) and (Price and Price[0] > 0):
                    TotalProduct += 1
                    ParsedData = self.Scheme.Data['product']['pipe']
                EscForSQL(ParsedData)

            await self.Api.ExecModel(
                'ctrl',
                {
                    'method': 'InsHistUrl',
                    'param': {
                        'aUrlId': Rec.url_id,
                        'aStatusCode': Data['status'],
                        'aParsedData': ParsedData,
                        'aUrlCount': UrlCount,
                        'aDataSize': DataSize,
                        'aUserId': self.Api.DbConf['user_id']
                    }
                }
            )

            Percentage = round(random.uniform(0.75, 1.0), 2)
            Sleep = float(self.DblSite.Rec.sleep_seconds) * Percentage
            await asyncio.sleep(Sleep)

        return {
            'hrefs': len(TotalHref),
            'tasks': self.DblUrl.GetSize(),
            'products': TotalProduct,
            'data_size': TotalDataSize
        }
