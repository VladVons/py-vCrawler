# Created: 2024.04.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Sql.DbModel import TDbModel


class TMain(TDbModel):
    async def Get_UserConf(self, aUserId: int) -> dict:
        return await self.ExecQuery(
            'fmtGet_UserConf.sql',
            {'aUserId': aUserId}
        )

    async def Get_UserId(self, aLogin: str, aPassw: str) -> dict:
        return await self.ExecQuery(
            'fmtGet_UserId.sql',
            {'aLogin': aLogin, 'aPassw': aPassw}
        )
