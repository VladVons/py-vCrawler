# Created: 2024.04.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Sql.DbModel import TDbModel

class TMain(TDbModel):
    async def Get_Tables(self, aSchema: str) -> dict:
        return await self.ExecQuery(
            'fmtGet_Tables.sql',
            {'aSchema': aSchema}
        )
