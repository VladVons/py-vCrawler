# Created: 2024.04.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Sql.DbModel import TDbModel


class TMain(TDbModel):
    async def GetAliasTranslate(self, aLang: str, aText: list[str]) -> dict:
        Arr = [f"('{xText}')" for xText in aText]

        return await self.ExecQuery(
            'fmtGet_AliasTranslate.sql',
            {
              'aLang': aLang,
              'aValues': ', '.join(Arr)
            }
        )
