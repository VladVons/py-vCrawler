# Created: 2024.10.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.DbList import TDbList
from Inc.ParserX.Common import TPluginBase
from .Main import TSchemer
from .. import SiteCondEnabled


class TSchemeTest(TPluginBase):
    async def Run(self):
        Dbl = TDbList().Import(self.Conf['sites'])
        Dbl = SiteCondEnabled(Dbl)
        for Rec in Dbl:
            Dir = f'{self.Conf["dir_data"]}/{Rec.dir}'
            Schemer = TSchemer(Dir)
            for xType in Rec.type:
                if (not xType.startswith('-')):
                    await Schemer.Test(xType)
