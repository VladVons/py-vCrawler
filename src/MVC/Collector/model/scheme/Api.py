# Created: 2024.10.31
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Sql.DbModel import TDbModel


class TMain(TDbModel):
    async def GetSchemeRnd(self) -> dict:
        return await self.ExecQuery(
            'fmtGet_SchemeRnd.sql',
            {}
        )
