# Created: 2024.04.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.DataClass import DDataClass
from IncP.ApiBase import TApiBase
from IncP.Plugins import TCrawlers
import IncP.LibCrawler as Lib


@DDataClass
class TUserConf():
    user_id: int = -1
    workers_allow: bool = True
    workers_qty: int = 1
    workers_sleep: int = 10
    main_sleep: int = 60
    speed_test_url: str = ''


class TApiCrawler(TApiBase):
    def __init__(self):
        super().__init__()

        self.DbConf: TUserConf = None

        Conf = self.GetConf()
        self.Conf = {
            'db_auth': Conf['db_auth']
        }

        self.Plugin = TCrawlers(Conf['dir_route'], self)
        self.InitLoader(Conf['loader'])
        self.ApiModel = self.Loader['model'].Get

    async def ExecModel(self, aMethod: str, aData: dict) -> Lib.TDbList:
        Res = await self.ApiModel(aMethod, aData)
        if (isinstance(Res, dict) and ('tag' in Res)):
            Res = Lib.TDbList().Import(Res)
        return Res

class TApiCrawlerEx(TApiCrawler):
    async def GetUserExt(self) -> TUserConf:
        Res = await self.Exec(
            'user',
            {
                'method': 'GetUserExt',
                'param': {
                   'aLogin': self.Conf['db_auth']['login'],
                   'aPassw': self.Conf['db_auth']['passw'],
                }
            }
        )

        if (Res is None):
            Res = {}
        return TUserConf(**Res)

    async def GetTask(self):
        Res = await self.ExecModel(
            'ctrl',
            {
                'method': 'GetTask',
                'param': {
                    'aUserId': self.DbConf.user_id
                }
            }
        )

        for Key in ['site', 'url']:
            Res[Key] = Lib.TDbList().Import(Res[Key])
        return Res

ApiCrawler = TApiCrawlerEx()
