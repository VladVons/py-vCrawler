# Created: 2024.04.19
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


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
