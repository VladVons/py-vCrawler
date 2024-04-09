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
from .WebScraper import TWebScraper


class TCrawler(TSrvBaseEx):
    def _GetDefRoutes(self) -> list:
        return [
            web.get('/api/{name:.*}', self._rApi)
        ]

    def GetApi(self) -> object:
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
            ApiCrawler.DbConf = await ApiCrawler.GetUserExt()
            if (ApiCrawler.DbConf):
                try:
                    MaxWorkers = await ApiCrawler.GetMaxWorkers()
                    await self._CreateTasks(MaxWorkers)
                except Exception as E:
                    Log.Print(1, 'x', 'Run()', aE = E)
            else:
                Log.Print(1, 'i', 'Auth error')
            await asyncio.sleep(60)

    async def _Worker(self, aTaskId: int):
        Log.Print(1, 'i', '_Worker(). Start Id %d' % (aTaskId))
        while (True):
            Wait = random.randint(1, 2)
            await asyncio.sleep(Wait)
            Data = await ApiCrawler.GetSiteUrlToUpdate()
            if (Data['url']):
                Scraper = TWebScraper(ApiCrawler, Data)
                await Scraper.Exec()


    async def _CreateTasks(self, aMaxTasks):
        Tasks = [asyncio.create_task(self._Worker(i)) for i in range(aMaxTasks)]
        await asyncio.gather(*Tasks)
