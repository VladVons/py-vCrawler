# Created: 2024.04.07
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Misc.Profiler import TTimerLog
from Task.Crawler.Api import TApiCrawler
import IncP.LibCrawler as Lib


class TCrawlerBase():
    def __init__(self, aApiCrawler: TApiCrawler):
        self.ApiCrawler = aApiCrawler
        self.ApiCtrl = None

    def _init_(self):
        self.ApiCtrl = self.ApiCrawler.Loader['ctrl'].Get

    async def ExecCtrl(self, aMethod: str, aData: dict) -> dict:
        with TTimerLog('ApiCtrl', False, aFile = 'Timer'):
            Res = await self.ApiCtrl(aMethod, aData)
            if (isinstance(Res, dict) and ('tag' in Res)):
                Res = Lib.TDbList().Import(Res)
        return Res

    async def ExecSelf(self, aRoute: str, aData: dict) -> dict:
        return await self.ApiCrawler.Exec(aRoute, aData)
