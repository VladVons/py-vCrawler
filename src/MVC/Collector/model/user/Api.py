# Created: 2024.04.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibModel as Lib


class TMain(Lib.TDbModel):
    async def GetUserExt(self, aUserId: int) -> dict:
        return await self.ExecQuery(
            'fmtGet_UserExt.sql',
            {'aUserId': aUserId}
        )

    async def GetUserId(self, aLogin: str, aPassw: str) -> dict:
        return await self.ExecQuery(
            'fmtGet_UserId.sql',
            {'aLogin': aLogin, 'aPassw': aPassw}
        )
