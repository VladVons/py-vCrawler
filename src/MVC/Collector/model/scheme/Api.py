# Created: 2024.10.31
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import json
import IncP.LibModel as Lib


class TMain(Lib.TDbModel):
    async def GetSchemeRnd(self) -> dict:
        return await self.ExecQuery(
            'fmtGet_SchemeRnd.sql',
            {}
        )

    async def GetSchemeNew(self) -> dict:
        return await self.ExecQuery(
            'fmtGet_SchemeNew.sql',
            {}
        )

    async def GetSchemeModerate(self) -> dict:
        return await self.ExecQuery(
            'fmtGet_SchemeModerate.sql',
            {}
        )

    async def UpdReserveTask(self, aUrl: str, aHours: int) -> dict:
        return await self.ExecQuery(
            'fmtUpd_ReserveTask.sql',
            {
              'aUrl': aUrl,
              'aHours': aHours
            }
        )

    async def UpdScheme(self, aSiteId: str, aUrlEn: str, aScheme: str) -> dict:
        Values = f"({aSiteId}, '{aUrlEn}'::url_enum, '{aScheme}'::json)"
        return await self.ExecQuery(
            'fmtUpd_Scheme.sql',
            {
              'aValues': Values
            }
        )

    async def GetProductsRnd(self, aLimit: int = 100) -> dict:
        return await self.ExecQuery(
            'fmtGet_ProductsRnd.sql',
            {
              'aLimit': aLimit
            }
        )

    async def GetProductsNoAttr(self, aLimit: int = 1000) -> dict:
        return await self.ExecQuery(
            'fmtGet_ProductsNoAttr.sql',
            {
              'aLimit': aLimit
            }
        )

    async def UpdProductsAttr(self, aValues: tuple) -> dict:
        Values = []
        for xUrlId, xTitle, xAttr in aValues:
            Attr = json.dumps(xAttr, ensure_ascii=False).replace("'", '`')
            Title = xTitle.replace("'", "''")
            Values.append(f"({xUrlId}, '{Title}', '{Attr}'::jsonb)")

        return await self.ExecQuery(
            'fmtUpd_ProductsAttr.sql',
            {
              'aValues': ', '.join(Values)
            }
        )
