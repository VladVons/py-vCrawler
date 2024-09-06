# Created: 2024.04.08
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import random
import asyncio
from urllib.parse import urljoin
#
from Inc.Scheme.Scheme import TScheme
from Inc.Util.Str import StartsWith
from Inc.Util.Obj import Iif, IifNone
from .Api import TApiCrawlerEx
from .Lib import Protego, GetUrlData, GetSoup, InitRobots, IsMimeApp, EscForSQL


def WriteFileDebug(aFile: str, aData):
    with open(aFile, 'wb') as F:
        F.write(aData)


class TWebScraper():
    def __init__(self, aApi: TApiCrawlerEx, aData: dict):
        self.Api = aApi
        self.DblSite = aData['site']
        self.DblUrl = aData['url']
        self.UrlRoot = self.DblSite.Rec.url
        self.Robots: Protego

    def GetHrefs(self, aSoup) -> set:
        Res = set()
        for xUrl in aSoup.find_all('a'):
            xUrl = xUrl.get('href', '').strip().rstrip('/')
            if (not xUrl) or \
               (len(xUrl) > 254) or \
               (StartsWith(xUrl, ['#', 'javascript:', 'tel:', 'mailto:', 'viber:', 'tg:', 'sms:'])) or \
               ((xUrl.startswith('http')) and (not xUrl.startswith(self.UrlRoot))) or \
               (IsMimeApp(xUrl)) or \
               (not self.Robots.can_fetch(xUrl, '*')):
                continue

            xUrl = xUrl.rsplit('#', maxsplit=1)[0]
            xUrl = urljoin(self.UrlRoot, xUrl)
            Res.add(xUrl.rstrip('/'))
        return Res

    async def Exec(self) -> dict:
        CustomRobots = self.DblSite.Rec.robots
        self.Robots = await InitRobots(self.UrlRoot, CustomRobots)

        TotalProduct = 0
        TotalDataSize = 0
        TotalHref = set()
        for Rec in self.DblUrl:
            UrlCount = 0
            DataSize = 0
            SchemeName = None
            Pipe = None

            Data = await GetUrlData(Rec.url, self.DblSite.Rec.headers)

            #Url = 'https://lux-pc.com/catalog/pos'
            #Data = await GetUrlData(Url, self.DblSite.Rec.headers)
            #WriteFileDebug('debug.html', Data['data'])

            if (Data['status'] == 200):
                DataSize = len(Data['data'])
                TotalDataSize += DataSize

                Soup = GetSoup(Data['data'])

                Schemes = {Key: Val for Data in self.DblSite.Rec.scheme for Key, Val in Data.items()}
                for Key, Val in Schemes.items():
                    Scheme = TScheme({Key: Val})
                    Scheme.Parse(Soup)
                    Pipe = Scheme.GetPipe(Key)
                    if (Key == 'product'):
                        Price = Pipe.get('price')
                        if (Pipe.get('name')) and \
                        (
                            (Price and isinstance(Price[0], (int, float)) and Price[0] > 0) or \
                            (Pipe.get('description') and Pipe.get('features'))
                        ):
                            SchemeName = Key
                            TotalProduct += 1
                            EscForSQL(Pipe)
                            break
                    elif (Key == 'category'):
                        if (len(Pipe.get('products', [])) > 1):
                            SchemeName = Key
                            break

                Htrefs = []
                AllowCategory = self.DblSite.Rec.category
                if (AllowCategory):
                    if (SchemeName == 'category'):
                        Products = [xProduct['href'] for xProduct in  Pipe['products']]
                        Categories = IifNone(Pipe.get('pager'), [])
                        Htrefs = set(Products + Categories)
                else:
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

            await self.Api.ExecModel(
                'ctrl',
                {
                    'method': 'InsHistUrl',
                    'param': {
                        'aUrlId': Rec.url_id,
                        'aStatusCode': Data['status'],
                        'aParsedData': Iif(SchemeName == 'product', Pipe, None),
                        'aUrlCount': UrlCount,
                        'aDataSize': DataSize,
                        'aUrlEn': SchemeName,
                        'aUserId': self.Api.DbConf.user_id
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
