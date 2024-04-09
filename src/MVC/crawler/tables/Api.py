# Created: 2024.04.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.CtrlBase import TCtrlBase


class TMain(TCtrlBase):
    async def GetTables(self) -> dict:
        Dbl = await self.ExecModelImport(
            'tables',
            {
                'method': 'GetTables',
                'param': {
                   'aSchema': 'public'
                }
            }
        )
        return Dbl.Export()
