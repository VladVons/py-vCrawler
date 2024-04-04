# Created: 2024.04.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.CtrlBase import TCtrlBase, Lib


class TMain(TCtrlBase):
    async def Main(self, aData: dict) -> dict:
        Dbl = await self.ExecModelImport(
            'system/test',
            {
                'method': 'Get_Tables',
                'param': {
                   'aSchema': 'public'
                }
            }
        )
        Dbl.Tag = aData['param']
        return Dbl.Export()
