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


class TApiCrawler(TApiBase):
    def __init__(self):
        super().__init__()

        self.DbConf: TUserConf

        Conf = self.GetConf()
        self.Conf = {
            'auth': Conf['auth']
        }

        self.Plugin = TCrawlers(Conf['dir_route'], self)
        self.InitLoader(Conf['loader'])
        self.ApiModel = self.Loader['model'].Get

    async def ExecModel(self, aMethod: str, aData: dict) -> dict:
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
                   'aLogin': self.Conf['auth']['login'],
                   'aPassw': self.Conf['auth']['passw'],
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
