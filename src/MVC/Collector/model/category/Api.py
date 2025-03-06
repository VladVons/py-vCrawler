# Created: 2024.12.10
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import json
import IncP.LibModel as Lib


class TMain(Lib.TDbModel):
    async def GetAttrCountCategoryCountry(self, aCountryId: int, aCategory: str) -> dict:
        return await self.ExecQuery(
            'fmtGet_AttrCountCategoryCountry.sql',
            {
                'aCountryId': aCountryId,
                'aCategory': aCategory
            }
        )

    async def GetAttrCountCategorySite(self, aSiteId: int, aCategory: str) -> dict:
        return await self.ExecQuery(
            'fmtGet_AttrCountCategorySite.sql',
            {
                'aSiteId': aSiteId,
                'aCategory': aCategory
            }
        )

    async def GetAttrCountFilterCountry(self, aCountryId: int, aFilter: dict) -> dict:
        Filter = aFilter.copy()
        PriceMin = Filter.pop('price_min', 0)
        PriceMax = Filter.pop('price_max', 10**10)

        Attr = json.dumps(Filter)
        return await self.ExecQuery(
            'fmtGet_AttrCountFilterCountry.sql',
            {
                'aCountryId': aCountryId,
                'aAttr': Attr,
                'aPriceMin': PriceMin,
                'aPriceMax': PriceMax
            }
        )

    async def GetAttrCountFilterSite(self, aSiteId: int, aFilter: dict) -> dict:
        Filter = aFilter.copy()
        PriceMin = Filter.pop('price_min', 0)
        PriceMax = Filter.pop('price_max', 10**10)

        Attr = json.dumps(Filter)
        return await self.ExecQuery(
            'fmtGet_AttrCountFilterSite.sql',
            {
                'aSiteId': aSiteId,
                'aAttr': Attr,
                'aPriceMin': PriceMin,
                'aPriceMax': PriceMax
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
