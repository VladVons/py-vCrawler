# Created: 2024.04.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.ApiBase import TApiBase
from IncP.Plugins import TCrawlers
import IncP.LibCrawler as Lib

class TApiCrawler(TApiBase):
    def __init__(self):
        super().__init__()

        self.DbConf = {}

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
    async def GetUserExt(self):
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
        Data = await self.ExecModel(
            'ctrl',
            {
                'method': 'GetSiteUrlToUpdate'
            }
        )

        return {
            'site': Lib.TDbList().Import(Data['site']),
            'url': Lib.TDbList().Import(Data['url'])
        }

ApiCrawler = TApiCrawlerEx()
