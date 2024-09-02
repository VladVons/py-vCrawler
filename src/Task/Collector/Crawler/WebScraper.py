# Created: 2024.04.08
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import random
import asyncio
from urllib.parse import urljoin
#
from Inc.Scheme.Scheme import TScheme
from Inc.Util.Str import StartsWith
from .Api import TApiCrawlerEx
from .Lib import Protego, GetUrlData, GetSoup, InitRobots, IsMimeApp, EscForSQL


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

            Data = await GetUrlData(Rec.url, self.DblSite.Rec.headers)

            # Url = 'https://acomp.com.ua/ua/mysh-igrovaya-hator-pulsar-htm-313-bu/'
            # Data = await GetUrlData(Url, self.DblSite.Rec.headers)
            # with open('debug.html', 'wb') as F:
            #      F.write(Data['data'])

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
                Pipe = self.Scheme.GetPipe()
                Price = Pipe.get('price')
                if (Pipe.get('name')) and \
                   (
                       (Price and isinstance(Price[0], (int, float)) and Price[0] > 0) or \
                       (Pipe.get('description') and Pipe.get('features'))
                   ):
                    TotalProduct += 1
                    EscForSQL(Pipe)
                else:
                    Pipe = None

            await self.Api.ExecModel(
                'ctrl',
                {
                    'method': 'InsHistUrl',
                    'param': {
                        'aUrlId': Rec.url_id,
                        'aStatusCode': Data['status'],
                        'aParsedData': Pipe,
                        'aUrlCount': UrlCount,
                        'aDataSize': DataSize,
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
