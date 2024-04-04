# Created: 2024.04.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.ApiBase import TApiBase
from IncP.Plugins import TCtrls


class TApiCtrl(TApiBase):
    def __init__(self, aName: str):
        super().__init__()

        self.Name = aName
        Conf = self.GetConf()[aName]
        self.Ctrls = TCtrls(Conf['dir_route'], self)
        self.InitLoader(Conf['loader'])
        self.DefRoute = 'system/def_route'

        # some options are in DB
        self.Conf = {
            'seo_url': Conf.get('seo_url', False)
        }

    async def Exec(self, aRoute: str, aData: dict) -> dict:
        if (self.ExecCnt == 0):
            await self.ExecOnce(aData)
        self.ExecCnt += 1

        Res = self.GetMethod(self.Ctrls, aRoute, aData)
        if ('err' not in Res):
            Res = await Res['method'](aData)
        return Res

ApiCtrls = {
    'main': TApiCtrl('main')
}
