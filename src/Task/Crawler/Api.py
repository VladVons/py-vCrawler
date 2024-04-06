# Created: 2024.04.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.DbList import TDbList
from IncP.ApiBase import TApiBase
from IncP.Plugins import TCrawlers


class TApiCrawler(TApiBase):
    def __init__(self):
        super().__init__()

        self.DbConf = {}

        Conf = self.GetConf()
        self.Conf = {
            'auth': Conf['auth']
        }
        self.Plugin = TCrawlers(Conf['dir_route'])
        self.InitLoader(Conf['loader'])
        self.DefRoute = 'system/def_route'

    async def Exec(self, aRoute: str, aData: dict) -> dict:
        if (self.ExecCnt == 0):
            await self.ExecOnce(aData)
        self.ExecCnt += 1

        Res = self.GetMethod(self.Plugin, aRoute, aData)
        if ('err' not in Res):
            Param = aData['param']
            Res = await Res['method'](Res['module'], **Param)
        return Res

    async def ExecCtrl(self, aRoute: str, aData: dict) -> dict:
        Res = await self.Loader['ctrl'].Get(aRoute, aData)
        if (isinstance(Res, dict) and ('tag' in Res)):
            Res = TDbList().Import(Res)
        return Res

class TApiCrawlerEx(TApiCrawler):
    async def GetUserConfig(self):
        Dbl = await self.ExecCtrl(
            'user',
            {
                'method': 'Get_UserId',
                'param': {
                   'login': self.Conf['auth']['login'],
                   'passw': self.Conf['auth']['passw'],
                }
            }
        )
        if (Dbl):
            UserId = Dbl.Rec.id
            Dbl = await self.ExecCtrl(
                'user',
                {
                    'method': 'Get_UserConf',
                    'param': {
                    'aUserId': UserId
                    }
                }
            )
            Res = {Rec.attr: Rec.val[0] for Rec in Dbl if Rec.val}
            Res['user_id'] = UserId
            return Res

    async def GetMaxWorkers(self) -> int:
        Res = int(self.DbConf.get('max_workers', 0))
        if (Res == 0):
            Time = await self.Exec(
                'system',
                {
                    'method': 'GetDownloadSpeed',
                    'param': {
                        'aUrl': self.DbConf['speed_test_url']
                    }
                }
            )
            Res = Time // 5
        return Res

    async def GetSiteUrlToUpdate(self):
        Res = await self.ExecCtrl(
            'site',
            {
                'method': 'Get_SiteUrlToUpdate',
                'param': {
                    'aLimit': 10
                }
            }
        )
        return Res

ApiCrawler = TApiCrawlerEx()
