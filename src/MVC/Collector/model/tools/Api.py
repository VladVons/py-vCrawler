# Created: 2025.01.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibModel as Lib


class TMain(Lib.TDbModel):
    async def Get_HistSession(self, aLimit: int, aOffset: int, aHaving: int = 1) -> dict:
        return await self.ExecQuery(
            'fmtGet_HistSession2.sql',
            {
                'aLimit': aLimit,
                'aOffset': aOffset,
                'aHaving': aHaving
            }
        )

    async def Get_HistUniqIpPerDay(self, aLimit: int, aOffset: int,) -> dict:
        return await self.ExecQuery(
            'fmtGet_HistUniqIpPerDay.sql',
            {
                'aLimit': aLimit,
                'aOffset': aOffset
            }
        )
