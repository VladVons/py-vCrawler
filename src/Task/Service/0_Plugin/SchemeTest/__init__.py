# Created: 2024.10.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.DbList import TDbList
from Inc.ParserX.Common import TPluginBase
from IncP.Log import Log
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
                    print()
                    Log.Print(1, 'i', f'Process {Dir}')
                    await Schemer.Test(xType)
                    if (self.Conf.get('pause', True)):
                        input('press enter to continue')
