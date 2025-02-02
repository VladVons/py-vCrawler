# Created: 2024.04.08
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import random
import asyncio
import json
from urllib.parse import urljoin
#
from Inc.Scheme.Scheme import TScheme
from Inc.Var.Dict import DeepSetByList, ToHash, GetNotNone
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


    def CheckAdd(self, aUrl: str) -> bool:
        return (isinstance(aUrl, str)) and (5 < len(aUrl.strip()) <= 256) and (aUrl not in self.Data)

    def Add(self, aUrl: str):
        if (self.CheckAdd(aUrl)):
            self.Data[aUrl] = [0, 0]

    def AddList(self, aUrl: list[str]):
        for xUrl in aUrl:
            self.Add(xUrl)

    def AddSafe(self, aUrl: str):
        if (not self.CheckAdd(aUrl)):
            return

        aUrl = aUrl.strip()
        if (StartsWith(aUrl, ['#', 'javascript:', 'tel:', 'mailto:', 'viber:', 'tg:', 'sms:'])) or \
            ((aUrl.startswith('http')) and (not aUrl.startswith(self.UrlRoot))) or \
            (IsMimeApp(aUrl)) or \
            (not self.Robots.can_fetch(aUrl, '*')):
            return

        aUrl = aUrl.rsplit('#', maxsplit=1)[0]
        aUrl = urljoin(self.UrlRoot, aUrl)
        self.Data[aUrl] = [0, 0]

    def Get(self, aUrl: str) -> list:
        return self.Data.get(aUrl, [0, 0])

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

        Pairs = Dbl.ExportPairs('url', ['id', 'crc'])
        self.Data.update(Pairs)

    async def Update(self):
        Urls = [xKey for xKey, xVal in self.Data.items() if xVal[0] == 0]
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
    def AdjustProduct(aData: dict, aUrl: str):
        aData['url'] = aUrl
        if (not aData.get('image')) and (aData.get('images')):
            aData['image'] = aData['images'][0]
        EscForSQL(aData)

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

        Proxy = self.DblSite.Rec.proxy
        if (Proxy) and (not Proxy.get('required')):
            if (Proxy.get('required') is None):
                Rnd = random.randint(1, Proxy['total'] * 2)
                if (Rnd >= Proxy['total']):
                    Proxy = None
            else:
                Proxy = None

        TotalProduct = 0
        TotalDataSize = 0
        for Rec in self.DblUrl:
            self.Cnt += 1
            DataSize = 0
            SchemeName = None
            Pipe = None

            Log.Print(2, 'i', f'TWebDcraper. Parse {Rec.url}')
            Schemes = self.JoinScheme(self.DblSite.Rec.scheme)
            StatusOnly = bool((Rec.url_en) and (Rec.url_en not in Schemes))

            Url = Rec.url
            # Url = 'https://www.olx.ua/d/uk/obyavlenie/noutbuk-dlya-raboty-i-ucheby-dell-latitude-5500-core-i5-8365u-podarok-IDX2lc4.html'
            # StatusOnly = False

            if (self.DblSite.Rec.emulator):
                Data = await PW_UrlGetData(Url, aStatusOnly=StatusOnly)
            else:
                Data = await UrlGetData(Url, self.DblSite.Rec.headers, aStatusOnly=StatusOnly, aProxy=Proxy)
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
                                self.AdjustProduct(Pipe, Url)
                                SchemeName = xKey
                                TotalProduct += 1
                                break
                        case 'category' | 'prodcat':
                            Products = IifNone(Pipe.get('products'), [])
                            if (len(Products) > 1):
                                SchemeName = xKey
                                break

                ParsedData = Iif(SchemeName == 'product', Pipe, None)
                Crc = ToHash(ParsedData)
                if (Crc != Rec.crc):
                    await self.Api.ExecModel(
                        'ctrl',
                        {
                            'method': 'InsUrlData',
                            'param': {
                                'aUrlId': Rec.url_id,
                                'aStatusCode': Status,
                                'aParsedData': ParsedData,
                                'aCrc': Crc,
                                'aUrlCount': len(RefUrl.Data),
                                'aDataSize': DataSize,
                                'aUserId': self.Api.DbConf.user_id,
                                'aUrlEn': SchemeName
                            }
                        }
                    )
                else:
                    print('CRC ok')

                if (self.DblSite.Rec.category):
                    if (SchemeName in ('category', 'prodcat')):
                        HrefProducts = [xProduct['href'] for xProduct in Products if ('href' in xProduct)]
                        RefUrl.AddList(HrefProducts)

                        HrefCategories = Pipe.get('pager')
                        if (HrefCategories):
                            RefUrl.AddList(HrefCategories)
                else:
                    for xUrl in Soup.find_all('a'):
                        RefUrl.AddSafe(xUrl)
                await RefUrl.Update()

                if (SchemeName == 'prodcat'):
                    Products = Pipe.get('products')
                    if (Products):
                        for xProduct in Products:
                            Href = xProduct.get('href')
                            if (Href) and (UrlId := RefUrl.Get(Href)[0]) and (self.IsProduct(xProduct)):
                                UrlEn = 'product'
                                await self.Api.ExecModel(
                                    'ctrl',
                                    {
                                        'method': 'UpdUrl',
                                        'param': {
                                            'aUrlId': UrlId,
                                            'aStatusCode': 200,
                                            'aUrlEn': UrlEn
                                        }
                                    }
                                )

                                self.AdjustProduct(xProduct, Href)
                                Crc = ToHash(xProduct)
                                if (Crc != RefUrl.Get(Href)[1]):
                                    await self.Api.ExecModel(
                                        'ctrl',
                                        {
                                            'method': 'InsUrlData',
                                            'param': {
                                                'aUrlId': UrlId,
                                                'aStatusCode': 200,
                                                'aParsedData': xProduct,
                                                'aCrc': Crc,
                                                'aUrlCount': 0,
                                                'aDataSize': 0,
                                                'aUserId': self.Api.DbConf.user_id,
                                                'aUrlEn': UrlEn
                                            }
                                        }
                                    )
                                    await asyncio.sleep(1)
            ProxyId = GetNotNone(Proxy, 'id', None)
            await self.Api.ExecModel(
                'ctrl',
                {
                    'method': 'UpdUrl',
                    'param': {
                        'aUrlId': Rec.url_id,
                        'aStatusCode': Status,
                        'aUrlEn': SchemeName,
                        'aProxyId': ProxyId
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
