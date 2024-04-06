# Created: 2024.04.06
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.CtrlBase import TCtrlBase, Lib


class TMain(TCtrlBase):
    async def Get_SiteUrlToUpdate(self, aData: dict) -> dict:
        aLimit = 10
        Dbl = await self.ExecModelImport(
            'site',
            {
                'method': 'Get_SiteUrlToUpdate',
                'param': {
                   'aLimit': aLimit
                }
            }
        )
        return Dbl.Export()
