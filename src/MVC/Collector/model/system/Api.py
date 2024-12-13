# Created: 2024.04.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Sql.DbModel import TDbModel


class TMain(TDbModel):
   async def GetAliasTranslate(self, aLang: str, aAlias: list[str]) -> dict:
        Arr = [f"('{xAlias}')" for xAlias in aAlias]

        return await self.ExecQuery(
            'fmtGet_AliasTranslate.sql',
            {
              'aLang': aLang,
              'aValues': ', '.join(Arr)
            }
        )
