# Created: 2024.04.19
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
#
from Inc.Sql.DbModel import TDbModel
import IncP.LibModel as Lib


class TMain(TDbModel):
    async def GetProductInfoBySku(self, aSiteId: int, aSkus: list[str]) -> dict:
        Skus = Lib.ListToComma(aSkus)
        return await self.ExecQuery(
            'fmtGet_ProductInfoBySkus.sql',
            {
                'aSiteId': aSiteId,
                'Skus': Skus
            }
        )

    async def Get_Products_Search1(self, aFilter: str, aOrder: str, aLimit: int = 100, aOffset: int = 0) -> dict:
        FilterRe = [f"('%{x}%')" for x in re.split(r'\s+', aFilter)]
        return await self.ExecQuery(
            'fmtGet_Products_Search1.sql',
            {
                'aFilter': aFilter,
                'FilterRe': ', '.join(FilterRe),
                'aOrder': aOrder,
                'aLimit': aLimit,
                'aOffset': aOffset
            }
        )
