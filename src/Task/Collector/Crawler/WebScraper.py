# Created: 2024.04.08
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import random
import asyncio
import json
from urllib.parse import urljoin
#
from Inc.Scheme.Scheme import TScheme
from Inc.Var.Str import StartsWith
from Inc.Var.Obj import Iif, IifNone
from Inc.Misc.PlayWrite import UrlGetData as PW_UrlGetData
from Inc.Misc.FS import WriteFileTyped
from .Api import TApiCrawlerEx
from .Lib import Protego, UrlGetData, GetSoup, InitRobots, IsMimeApp, EscForSQL


def WriteFileDebug(aFile: str, aData):
    aFile = aFile.replace(':', '').replace('/', '_') + '.html'
    WriteFileTyped(aFile, aData)


class TWebScraper():
    def __init__(self, aApi: TApiCrawlerEx, aData: dict):
        self.Api = aApi
        self.DblSite = aData['site']
        self.DblUrl = aData['url']
        self.UrlRoot = self.DblSite.Rec.url
        self.Robots: Protego
        self.Cnt = 0

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
            self.Cnt += 1
            UrlCount = 0
            DataSize = 0
            SchemeName = None
            Pipe = None

            Url = Rec.url
            #Url = 'https://pc.com.ua/ua/noutbuk-156-dell-inspiron-3501-intel-core-i5-1135g7-16gb-ram-240gb-ssd-fullhd-b-class'
            if (self.DblSite.Rec.emulator):
                Data = await PW_UrlGetData(Url)
            else:
                Data = await UrlGetData(Url, self.DblSite.Rec.headers)
            #WriteFileDebug(f'{Url}_{self.Cnt}', Data['data'])
            #await asyncio.sleep(3)
            #continue

            if (Data['status'] == 200):
                DataSize = len(Data['data'])
                TotalDataSize += DataSize

                Soup = GetSoup(Data['data'])

                Schemes = {}
                for xScheme in self.DblSite.Rec.scheme:
                    xScheme = json.loads(xScheme)
                    for Key, Val in xScheme.items():
                        Schemes[Key] = Val

                for Key, Val in Schemes.items():
                    Scheme = TScheme({Key: Val})
                    Scheme.Parse(Soup)
                    Pipe = Scheme.GetPipe(Key)
                    if (Key == 'product'):
                        Price = Pipe.get('price')
                        if (Pipe.get('name')) and \
                        (
                            (Price and isinstance(Price[0], (int, float)) and Price[0] > 0)
                            #or (Pipe.get('description') and Pipe.get('features'))
                        ):
                            Pipe['url'] = Url
                            if (not Pipe.get('image')) and (Pipe.get('images')):
                                Pipe['image'] = Pipe['images'][0]

                            SchemeName = Key
                            TotalProduct += 1
                            EscForSQL(Pipe)
                            break
                    elif (Key == 'category'):
                        Products = IifNone(Pipe.get('products'), [])
                        if (len(Products) > 1):
                            SchemeName = Key
                            break

                Htrefs = []
                AllowCategory = self.DblSite.Rec.category
                if (AllowCategory):
                    if (SchemeName == 'category'):
                        Products = [xProduct['href'] for xProduct in  Products if len(xProduct['href']) < 255]
                        Categories = IifNone(Pipe.get('pager'), [])
                        Htrefs = set(Products + Categories)
                else:
                    Htrefs = self.GetHrefs(Soup)
                #Debug = [print(x) for x in Htrefs]

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
