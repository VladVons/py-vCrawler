# Created: 2024.04.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.CtrlBase import TCtrlBase


class TMain(TCtrlBase):
    async def GetUserId(self, aLogin: str, aPassw: str) -> dict:
        Dbl = await self.ExecModelImport(
            'user',
            {
                'method': 'GetUserId',
                'param': {
                   'aLogin': aLogin,
                   'aPassw': aPassw
                }
            }
        )
        return Dbl.Export()

    async def GetUserExt(self, aUserId: int) -> dict:
        Dbl = await self.ExecModelImport(
            'user',
            {
                'method': 'GetUserExt',
                'param': {
                   'aUserId': aUserId
                }
            }
        )
        return Dbl.Export()
