# Created: 2023.09.26
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.ParserX.Common import TPluginBase
from .Main import TSchemer


class TSchemeTest(TPluginBase):
    async def Run(self):
        for xSite, xTypes in self.Conf.get('sites', []):
            if (not xSite.startswith('-')):
                Dir = f'{self.Conf["dir_data"]}/{xSite}'
                Schemer = TSchemer(Dir)
                for xType in xTypes:
                    if (not xType.startswith('-')):
                        await Schemer.Test(xType)
