# Created: 2024.12.10
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Sql.DbModel import TDbModel


class TMain(TDbModel):
    async def GetAttrCountInCategory(self, aCountryId: int, aCategory: str) -> dict:
        return await self.ExecQuery(
            'fmtGet_AttrCountInCategory.sql',
            {
                'aCountryId': aCountryId, 
                'aCategory': aCategory
            }
        )

