# Created: 2024.04.04
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from aiohttp import web
#
from IncP.SrvBaseEx import TSrvBaseEx
from IncP.Log import Log
from .Api import ApiCtrls


class TCrawler():
    async def GetMaxWorkers(self, aWorkers) -> int:
        Res = self.Conf.get('max_workers', aWorkers)
        if (not Res):
            Url = self.Conf.get('speed_test_url')
            if (Url):
                Speed = await TDownloadSpeed(Url, 2).Test()
                Res = round(Speed / 5)
            else:
                Res = 5
        return Res


   async def Run(self):
        WaitLocalHost = 2
        await asyncio.sleep(WaitLocalHost)

        while (True):
            try:
                #TaskWS = asyncio.create_task(self.WebSock.Connect('ws/api', {'id': 1}))

                DataApi = await Api.GetUserConfig()
                Err = FilterKeyErr(DataApi)
                if (Err):
                    Log.Print(1, 'e', 'Run() %s' % Err)
                else:
                    Dbl = TDbList().Import(DeepGet(DataApi, 'data.data'))
                    Conf = Dbl.ExportPair('name', 'data')
                    Workers = int(Conf.get('workers', 0))
                    MaxWorkers = await self.GetMaxWorkers(Workers)
                    await self._CreateTasks(MaxWorkers)
            except Exception as E:
                Log.Print(1, 'x', 'Run()', aE = E)
            await asyncio.sleep(10)
