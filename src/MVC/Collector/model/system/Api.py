# Created: 2024.04.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Sql.DbModel import TDbModel


class TMain(TDbModel):
    async def GetAliasLangByList(self, aLangId: int, aText: list[str]) -> dict:
        Arr = [f"('{xText}')" for xText in aText]

        return await self.ExecQuery(
            'fmtGet_AliasLangByList.sql',
            {
              'aLangId': aLangId,
              'aValues': ', '.join(Arr)
            }
        )

    async def GetAliasLang(self, aLangId: int) -> dict:
        return await self.ExecQuery(
            'fmtGet_AliasLang.sql',
            {
              'aLangId': aLangId
            }
        )

    async def GetLang(self, aLangId: int) -> dict:
        return await self.ExecQuery(
            'fmtGet_Lang.sql',
            {
              'aLangId': aLangId
            }
        )
