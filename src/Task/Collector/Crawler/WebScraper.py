# Created: 2024.04.08
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import random
import asyncio
import json
import zlib
from urllib.parse import urljoin
#
from Inc.Scheme.Scheme import TScheme
from Inc.Var.Dict import DeepSetByList
from Inc.Var.Str import StartsWith
from Inc.Var.Obj import Iif, IifNone
from Inc.Misc.PlayWrite import UrlGetData as PW_UrlGetData
from Inc.Misc.FS import WriteFileTyped
from IncP.Log import Log
from .Api import TApiCrawlerEx
from .Lib import Protego, UrlGetData, GetSoup, InitRobots, IsMimeApp, EscForSQL


def WriteFileDebug(aFile: str, aData):
    aFile = aFile.replace(':', '').replace('/', '_') + '.html'
    WriteFileTyped(aFile, aData)


class TRefUrl():
    def __init__(self, aParent):
        self.Parent = aParent
        self.Data = {}

    @property
    def Api(self):
        return self.Parent.Api

    @property
    def SiteId(self):
        return self.Parent.DblSite.Rec.id

    @property
    def UrlRoot(self):
        return self.Parent.UrlRoot

    @property
    def Robots(self):
        return self.Parent.Robots


    def Add(self, aUrl: str):
        self.Data[aUrl] = 0

    def AddList(self, aUrl: list[str]):
        for xUrl in aUrl:
            self.Add(xUrl)

    def AddSafe(self, aUrl: str):
        aUrl = aUrl.strip()
        if (not aUrl) or (len(aUrl) >= 255):
            return

        if (StartsWith(aUrl, ['#', 'javascript:', 'tel:', 'mailto:', 'viber:', 'tg:', 'sms:'])) or \
            ((aUrl.startswith('http')) and (not aUrl.startswith(self.UrlRoot))) or \
            (IsMimeApp(aUrl)) or \
            (not self.Robots.can_fetch(aUrl, '*')):
            return

        aUrl = aUrl.rsplit('#', maxsplit=1)[0]
        aUrl = urljoin(self.UrlRoot, aUrl)

    def GetId(self, aUrl: str) -> int:
        return self.Data.get(aUrl, 0)

    async def _Update(self, aUrls: list[str]):
        Dbl = await self.Api.ExecModel(
            'ctrl',
            {
                'method': 'InsUrls',
                'param': {
                    'aSiteId': self.SiteId,
                    'aUrls': aUrls
                }
            }
        )

        Pairs = Dbl.ExportPair('url', 'id')
        self.Data.update(Pairs)

    async def Update(self):
        Urls = [xKey for xKey, xVal in self.Data.items() if xVal == 0]
        if (Urls):
            await self._Update(Urls)


class TWebScraper():
    def __init__(self, aApi: TApiCrawlerEx, aData: dict):
        self.Api = aApi
        self.DblSite = aData['site']
        self.DblUrl = aData['url']
        self.UrlRoot = self.DblSite.Rec.url
        self.Robots: Protego
        self.Cnt = 0

    @staticmethod
    def JoinScheme(aSchemes: list[str]) -> dict:
        Res = {}
        for xScheme in aSchemes:
            xScheme = json.loads(xScheme)
            for Key, Val in xScheme.items():
                Res[Key] = Val
        return Res

    @staticmethod
    def AdjustProduct(aData: dict, aUrl: str) -> int:
        aData['url'] = aUrl
        if (not aData.get('image')) and (aData.get('images')):
            aData['image'] = aData['images'][0]
        EscForSQL(aData)

        Str = json.dumps(aData, sort_keys=True)
        return zlib.crc32(Str.encode()) & 0x7FFFFFFF

    @staticmethod
    def IsProduct(aData: dict) -> bool:
        Price = aData.get('price')
        Res = (aData.get('name')) and \
            (
                (Price and isinstance(Price[0], (int, float)) and Price[0] > 0)
                #or (Pipe.get('description') and Pipe.get('features'))
            )
        return Res

    async def Exec(self) -> dict:
        RefUrl = TRefUrl(self)

        CustomRobots = self.DblSite.Rec.robots
        self.Robots = await InitRobots(self.UrlRoot, CustomRobots)

        TotalProduct = 0
        TotalDataSize = 0
        for Rec in self.DblUrl:
            self.Cnt += 1
            DataSize = 0
            PipeCrc = 0
            SchemeName = None
            Pipe = None

            Log.Print(2, 'i', f'TWebDcraper. Parse {Rec.url}')
            Schemes = self.JoinScheme(self.DblSite.Rec.scheme)
            StatusOnly = bool((Rec.url_en) and (Rec.url_en not in Schemes))

            Url = Rec.url
            #Url = 'https://www.lapstore.com.ua/product/dell-precision-7540-core-i7-9850h-ram-32-gb-ssd-512-gb-15-6-4k-quadro-t2000-4-gb/'
            if (self.DblSite.Rec.emulator):
                Data = await PW_UrlGetData(Url, aStatusOnly=StatusOnly)
            else:
                Data = await UrlGetData(Url, self.DblSite.Rec.headers, aStatusOnly=StatusOnly)
            #WriteFileDebug(f'{Url}_{self.Cnt}', Data['data'])

            Status = Data['status']
            if (StatusOnly):
                SchemeName = Rec.url_en
            elif (Status == 200):
                DataSize = len(Data['data'])
                TotalDataSize += DataSize

                Soup = GetSoup(Data['data'])
                for xKey in ['product', 'category', 'prodcat']:
                    Val = Schemes.get(xKey)
                    if (not Val):
                        continue

                    DeepSetByList(Val, ['info', 'url'], [Url])
                    Scheme = TScheme({xKey: Val})
                    Scheme.Parse(Soup)
                    Pipe = Scheme.GetPipe(xKey)
                    Log.Print(3, 'i', f'TWebDcraper. {Scheme.Err}')
                    match xKey:
                        case 'product':
                            if (self.IsProduct(Pipe)):
                                PipeCrc = self.AdjustProduct(Pipe, Url)
                                SchemeName = xKey
                                TotalProduct += 1
                                break
                        case 'category' | 'prodcat':
                            Products = IifNone(Pipe.get('products'), [])
                            if (len(Products) > 1):
                                SchemeName = xKey
                                break

                await self.Api.ExecModel(
                    'ctrl',
                    {
                        'method': 'InsHistUrl',
                        'param': {
                            'aUrlId': Rec.url_id,
                            'aStatusCode': Status,
                            'aParsedData': Iif(SchemeName == 'product', Pipe, None),
                            'aCrc': PipeCrc,
                            'aUrlCount': len(RefUrl.Data),
                            'aDataSize': DataSize,
                            'aUserId': self.Api.DbConf.user_id
                        }
                    }
                )

                if (self.DblSite.Rec.category):
                    if (SchemeName in ('category', 'prodcat')):
                        Products = [xProduct['href'] for xProduct in Products if ('href' in xProduct)]
                        RefUrl.AddList(Products)

                        Categories = Pipe.get('pager')
                        if (Categories):
                            RefUrl.AddList(Categories)
                else:
                    for xUrl in Soup.find_all('a'):
                        RefUrl.AddSafe(xUrl)
                await RefUrl.Update()

                if (SchemeName == 'prodcat'):
                    Products = Pipe.get('products')
                    if (Products):
                        for xProduct in Products:
                            Href = xProduct.get('href')
                            if (Href) and (UrlId := RefUrl.GetId(Href)) and (self.IsProduct(xProduct)):
                                Crc = self.AdjustProduct(xProduct, Href)
                                await self.Api.ExecModel(
                                    'ctrl',
                                    {
                                        'method': 'UpdUrl',
                                        'param': {
                                            'aUrlId': UrlId,
                                            'aStatusCode': 200,
                                            'aUrlEn': 'product'
                                        }
                                    }
                                )

                                await self.Api.ExecModel(
                                    'ctrl',
                                    {
                                        'method': 'InsHistUrl',
                                        'param': {
                                            'aUrlId': UrlId,
                                            'aStatusCode': 200,
                                            'aParsedData': xProduct,
                                            'aCrc': Crc,
                                            'aUrlCount': 0,
                                            'aDataSize': 0,
                                            'aUserId': self.Api.DbConf.user_id
                                        }
                                    }
                                )
                                await asyncio.sleep(1)
            await self.Api.ExecModel(
                'ctrl',
                {
                    'method': 'UpdUrl',
                    'param': {
                        'aUrlId': Rec.url_id,
                        'aStatusCode': Status,
                        'aUrlEn': SchemeName
                    }
                }
            )

            Percentage = round(random.uniform(0.75, 1.0), 2)
            Sleep = float(self.DblSite.Rec.sleep_seconds) * Percentage
            await asyncio.sleep(Sleep)

        Res = {
            'hrefs': len(RefUrl.Data),
            'tasks': self.DblUrl.GetSize(),
            'products': TotalProduct,
            'data_size': TotalDataSize
        }
        return Res
