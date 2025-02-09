# Created: 2024.04.05
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

import random
import asyncio
from aiohttp import web
#
from Inc.Var.Dict import DictDiff
from Inc.Var.Obj import GetClassVars
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

    async def TestModel(self) -> dict:
        Res = await ApiCrawler.ExecModel(
            'product',
            {
                'method': 'GetProductInfoBySku',
                'param': {
                    'aSiteId': 2,
                    'aSkus': ['368313', '380932']
                }
            }
        )
        return Res

    async def _CreateTasks(self, aMaxTasks):
        Tasks = [asyncio.create_task(self._Worker(i+1)) for i in range(aMaxTasks)]
        await asyncio.gather(*Tasks)

    async def RunApi(self):
        Log.Print(1, 'i', f'{self.__class__.__name__}.RunApi()')
        Log.Print(1, 'i', f"Conf db_auth/login: {ApiCrawler.Conf['db_auth']['login']}")

        WaitLocalHost = 2
        await asyncio.sleep(WaitLocalHost)

        #await self.TestModel()

        while (True):
            DbConf = await ApiCrawler.GetUserExt()
            if (DbConf.user_id != -1):
                Arr = [f'{Key}: {Val}' for Key, Val in GetClassVars(DbConf).items()]
                Log.Print(1, 'i', f'RunApi(). {', '.join(Arr)}')

                try:
                    if (DbConf.workers_allow):
                        Log.Print(1, 'i', 'Task create')
                        await self._CreateTasks(DbConf.workers_qty)
                        Log.Print(1, 'i', 'Task done')
                except Exception as E:
                    Log.Print(1, 'x', 'Run()', aE = E)
            else:
                Log.Print(1, 'i', 'Auth error')

            await asyncio.sleep(DbConf.main_sleep)

    async def _Worker(self, aTaskId: int):
        Log.Print(1, 'i', f'_Worker({aTaskId :2}) started')

        Sleep = random.uniform(0, 2)
        await asyncio.sleep(Sleep)

        while (True):
            DbConf = await ApiCrawler.GetUserExt()
            if (DbConf.user_id == -1) or (not DbConf.workers_allow):
                break

            if (ApiCrawler.DbConf):
                Diff = DictDiff(DbConf.__dict__, ApiCrawler.DbConf.__dict__)
                if (Diff['changed']):
                    ApiCrawler.DbConf = DbConf
                    Log.Print(1, 'i', f'_Worker(). Conf changed: {Diff["mod"]}. Reload')
                    break
            ApiCrawler.DbConf = DbConf

            Sleep = random.uniform(DbConf.workers_sleep * 0.75, DbConf.workers_sleep)
            await asyncio.sleep(Sleep)

            Data = await ApiCrawler.GetTask()
            if ('err' in Data):
                Log.Print(1, 'i', Data['err'])
                continue

            if (Data['url']):
                Scraper = TWebScraper(ApiCrawler, Data)
                try:
                    Info = await Scraper.Exec()
                    Log.Print(1, 'i', f"user_id:{DbConf.user_id :2}, _Worker({aTaskId :2}/{DbConf.workers_qty: 2}), {Data['site'].Rec.url :30}, prod:{Info['products'] :2}/{Info['tasks'] :2}, hrefs:{Info['hrefs'] :4}, size:{Info['data_size']//1000 :5}Kb")
                except Exception as E:
                    Log.Print(1, 'x', f'_Worker(). {E}')

        Log.Print(1, 'i', f'_Worker({aTaskId :2}) finished')
