# Created: 2024.04.05
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

import random
import asyncio
from aiohttp import web
#
from IncP.SrvBaseEx import TSrvBaseEx
from IncP.Log import Log
from .Api import ApiCrawler


class TCrawler(TSrvBaseEx):
    def _GetDefRoutes(self) -> list:
        return [
            web.get('/api/{name:.*}', self._rApi)
        ]

    def _GetApi(self) -> object:
        return ApiCrawler

    async def RunApp(self):
        Log.Print(1, 'i', f'{self.__class__.__name__}.RunApp() on port {self._SrvConf.port}')

        ErroMiddleware = {
            404: self._Err_404,
            'err_all': self._Err_All
        }
        App = self.CreateApp(aErroMiddleware = ErroMiddleware)
        await self.Run(App)

    async def RunApi(self):
        Log.Print(1, 'i', f'{self.__class__.__name__}.RunApi() only')

        WaitLocalHost = 2
        await asyncio.sleep(WaitLocalHost)

        while (True):
            ApiCrawler.DbConf = await ApiCrawler.GetUserConfig()
            try:
                MaxWorkers = await ApiCrawler.GetMaxWorkers()
                await self._CreateTasks(MaxWorkers)
            except Exception as E:
                Log.Print(1, 'x', 'Run()', aE = E)
            await asyncio.sleep(60)

    async def _Worker(self, aTaskId: int):
        Log.Print(1, 'i', '_Worker(). Start Id %d' % (aTaskId))
        while (True):
            Wait = random.randint(2, 5)
            #Log.Print(1, 'i', '_Worker(). Ready for task. Id %d, wait %d sec' % (aTaskId, Wait))
            await asyncio.sleep(Wait)

            #await self.WebSock.Send({'data': 'Hellow from client. Id %s' % aTaskId})
            #continue

            DataApi = await ApiCrawler.GetSiteUrlToUpdate()
            # Data = DeepGet(DataApi, 'data.data')
            # if (Data):
            #     Scheme = TScheme(Data['scheme'])
            #     Type = Data.get('type')
            #     if (Type == 'full'):
            #         if (Data['sitemap']):
            #             Scraper = TWebScraperSitemap(self, Scheme, Data['url'], Data['id'], Data['sleep'])
            #         else:
            #             Scraper = TWebScraperFull(self, Scheme, Data['url'], Data['id'], Data['sleep'])
            #     elif (Type == 'update'):
            #         Scraper = TWebScraperUpdate(self, Scheme, Data['urls'], Data['sleep'])
            #     elif (Type == 'update_selenium'):
            #         #await TStarter().ThreadCreate(Data['urls'])
            #         continue
            #     else:
            #         Log.Print(1, 'e', '_Worker(). Unknown type: `%d`' % (Type))
            #         return

            #     self.Scrapers.append(Scraper)
            #     await Scraper._Worker()


    async def _CreateTasks(self, aMaxTasks):
        Tasks = [asyncio.create_task(self._Worker(i)) for i in range(aMaxTasks)]
        await asyncio.gather(*Tasks)
