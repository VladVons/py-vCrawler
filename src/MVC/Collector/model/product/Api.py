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
        reSite = re.compile(r'\b[a-z0-9.-]+\.[a-z]{2,3}(?:\.[a-z]{2,3})?\b')

        ArrAnd = []
        Words = re.split(r'\s+', aFilter)
        if (len(Words) == 1) and (re.search(r'\b\d{4,8}\b', Words[0])):
            ArrAnd.append(f'rp.url_id = {Words[0]}')
        else:
            for xWord in Words:
                Match = reSite.findall(xWord)
                if (Match):
                    ArrAnd.append(f"rs.url like '%{xWord}%'")
                else:
                    ArrAnd.append(f"rp.title ilike '%{xWord}%'")
        ExtWhere = 'and '.join(ArrAnd)

        return await self.ExecQuery(
            'fmtGet_Products_Search1.sql',
            {
                'aFilter': aFilter,
                'ExtWhere': ExtWhere,
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

    async def GetProductByUrlId(self, aUrlId: int, aLangId: int) -> dict:
        return await self.ExecQuery(
            'fmtGet_ProductByUrlId.sql',
            {
                'aUrlId': aUrlId,
                'aLangId': aLangId
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
