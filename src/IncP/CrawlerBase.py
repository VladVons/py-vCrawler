# Created: 2024.04.07
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Misc.Profiler import TTimerLog
from Task.Collector.Crawler.Api import TApiCrawler
import IncP.LibCrawler as Lib


class TCrawlerBase():
    def __init__(self, aApiCrawler: TApiCrawler):
        self.ApiCrawler = aApiCrawler
        self.ApiModel = None

    def _init_(self):
        self.ApiModel = self.ApiCrawler.Loader['model'].Get

    async def ExecModel(self, aMethod: str, aData: dict) -> dict:
        with TTimerLog('ApiModel', False, aFile = 'Timer'):
            Res = await self.ApiModel(aMethod, aData)
            if (isinstance(Res, dict) and ('tag' in Res)):
                Res = Lib.TDbList().Import(Res)
        return Res

    async def ExecSelf(self, aRoute: str, aData: dict) -> dict:
        return await self.ApiCrawler.Exec(aRoute, aData)
