# Created: 2024.12.10
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibModel as Lib


class TMain(Lib.TDbModel):
    async def GetAttrCountInCategory(self, aCountryId: int, aCategory: str, aSiteId: int = None) -> dict:
        WhereExt = ''
        if (aSiteId):
            WhereExt = f' and rs.id = {aSiteId}'

        return await self.ExecQuery(
            'fmtGet_AttrCountInCategory.sql',
            {
                'aCountryId': aCountryId,
                'aCategory': aCategory,
                'WhereExt': WhereExt
            }
        )

    async def GetAttrCountInCategorySite(self, aSiteId: int, aCategory: str) -> dict:
        return await self.ExecQuery(
            'fmtGet_AttrCountInCategorySite.sql',
            {
                'aSiteId': aSiteId,
                'aCategory': aCategory
            }
        )

    async def GetCategoriesCountry(self, aCountryId: int) -> dict:
        return await self.ExecQuery(
            'fmtGet_CategoriesCountry.sql',
            {
                'aCountryId': aCountryId
            }
        )

    async def GetCategoriesSite(self, aSiteId: int) -> dict:
        return await self.ExecQuery(
            'fmtGet_CategoriesSite.sql',
            {
                'aSiteId': aSiteId
            }
        )
