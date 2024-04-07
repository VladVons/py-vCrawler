# Created: 2024.04.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.ApiBase import TApiBase
from IncP.Plugins import TCtrls


class TApiCtrl(TApiBase):
    def __init__(self):
        super().__init__()

        Conf = self.GetConf()
        self.Plugin = TCtrls(Conf['dir_route'], self)
        self.InitLoader(Conf['loader'])
        self.DefRoute = 'system/def_route'

        # some options are in DB
        self.Conf = {
            'seo_url': Conf.get('seo_url', False)
        }


ApiCtrl = TApiCtrl()

