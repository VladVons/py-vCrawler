# Created: 2024.04.19
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
import json
#
import IncP.LibModel as Lib


class TMain(Lib.TDbModel):
    async def GetProductInfoBySku(self, aSiteId: int, aSkus: list[str]) -> dict:
        Skus = Lib.ListToComma(aSkus)
        return await self.ExecQuery(
            'fmtGet_ProductInfoBySkus.sql',
            {
                'aSiteId': aSiteId,
                'Skus': Skus
            }
        )

    async def Get_Products_Search1(self, aFilter: str, aCountryId: int, aOrder: str, aLimit: int = 100, aOffset: int = 0) -> dict:
        FilterRe = [f"('%{x}%')" for x in re.split(r'\s+', aFilter)]
        return await self.ExecQuery(
            'fmtGet_Products_Search1.sql',
            {
                'aFilter': aFilter,
                'FilterRe': ', '.join(FilterRe),
                'aCountryId': aCountryId,
                'aOrder': aOrder,
                'aLimit': aLimit,
                'aOffset': aOffset
            }
        )

    async def Get_Products_Search2(self, aFilter: str, aCountryId: int, aOrder: str, aLimit: int = 100, aOffset: int = 0) -> dict:
        aFilter = aFilter.replace('-', ' ').replace('/', ' ').strip('&').strip()
        aFilter = re.sub(r'\s+', '&', aFilter)

        return await self.ExecQuery(
            'fmtGet_Products_Search2.sql',
            {
                'aFilter': aFilter,
                'aCountryId': aCountryId,
                'aOrder': aOrder,
                'aLimit': aLimit,
                'aOffset': aOffset
            }
        )

    async def GetProductsAttrCountry(self, aFilter: dict, aCountryId: int, aOrder: str, aLimit: int = 25, aOffset: int = 0) -> dict:
        Filter = json.dumps(aFilter, ensure_ascii=False)
        return await self.ExecQuery(
            'fmtGet_ProductsAttrCountry.sql',
            {
                'aFilter': Filter,
                'aCountryId': aCountryId,
                'aOrder': aOrder,
                'aLimit': aLimit,
                'aOffset': aOffset
            }
        )

    async def GetProductsAttrSite(self, aFilter: dict, aSiteId: int, aOrder: str, aLimit: int = 25, aOffset: int = 0) -> dict:
        Filter = json.dumps(aFilter, ensure_ascii=False)
        return await self.ExecQuery(
            'fmtGet_ProductsAttrSite.sql',
            {
                'aFilter': Filter,
                'aSiteId': aSiteId,
                'aOrder': aOrder,
                'aLimit': aLimit,
                'aOffset': aOffset
            }
        )

    async def GetProductsAttrId(self, aUrlIds: list[int], aLimit: int = 25, aOffset: int = 0) -> dict:
        UrlIds = Lib.ListIntToComma(aUrlIds)
        return await self.ExecQuery(
            'fmtGet_ProductsAttrId.sql',
            {
                'aUrlIds': UrlIds,
                'aLimit': aLimit,
                'aOffset': aOffset
            }
        )

    async def GetProductByUrlId(self, aUrlId: int) -> dict:
        return await self.ExecQuery(
            'fmtGet_ProductByUrlId.sql',
            {
                'aUrlId': aUrlId
            }
        )

    async def GetProductByUrlIds(self, aUrlIds: list[int]) -> dict:
        UrlIds = Lib.ListIntToComma(aUrlIds)
        return await self.ExecQuery(
            'fmtGet_ProductByUrlIds.sql',
            {
                'aUrlIds': UrlIds
            }
        )

    async def GetProductsLastAdded(self, aCountryId: int, aLimit: int = 25) -> dict:
        return await self.ExecQuery(
            'fmtGet_ProductsLastAdded.sql',
            {
                'aCountryId': aCountryId,
                'aLimit': aLimit
            }
        )
