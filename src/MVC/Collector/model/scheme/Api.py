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
