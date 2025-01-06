# Created: 2024.04.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibModel as Lib

class TMain(Lib.TDbModel):
    async def GetTables(self, aSchema: str) -> dict:
        return await self.ExecQuery(
            'fmtGet_Tables.sql',
            {'aSchema': aSchema}
        )
