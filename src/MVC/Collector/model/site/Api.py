# Created: 2024.04.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import asyncio
import json
#
import IncP.LibModel as Lib

Lock = asyncio.Lock()


class TMain(Lib.TDbModel):
    async def GetSiteToUpdate(self) -> dict:
        return await self.ExecQuery(
            'fmtGet_SiteToUpdate.sql'
        )

    async def GetUrlToUpdate(self, aSiteId: int, aLimit: int) -> dict:
        return await self.ExecQuery(
            'fmtGet_UrlToUpdate.sql',
            {
                'aSiteId': aSiteId,
                'aLimit': aLimit
            }
        )

    async def GetUrlToUpdate_FromList(self, aSiteId: int, aUrls: list[str]) -> dict:
        Arr = [f"('{xUrl}')" for xUrl in aUrls]
        return await self.ExecQuery(
            'fmtGet_UrlToUpdate_FromList.sql',
            {
                'aSiteId': aSiteId,
                'Urls': ', '.join(Arr)
            }
        )

    async def SetUrlToUpdateLock(self, aSiteId: int, aUrlIds: list[int], aLimit: int) -> dict:
        UrlIds = Lib.ListIntToComma(aUrlIds)
        await self.ExecQuery(
            'fmtUpd_SiteUrlToUpdateLock.sql',
            {
                'aSiteId': aSiteId,
                'UrlIds': UrlIds,
                'aLimit': aLimit
            }
        )

    async def InsUrls(self, aSiteId: int, aUrls: list[str]) -> dict:
        Arr = [f'''({aSiteId}, '{xUrl.replace("'", "''")}')''' for xUrl in aUrls]
        return await self.ExecQuery(
            'fmtIns_Urls.sql',
            {
                'aValues': ', '.join(Arr)
            }
        )

    async def UpdUrl(self, aUrlId: int, aUrlEn: str, aStatusCode: int, aProxyId: int = None) -> dict:
        aProxyId = Lib.Iif(aProxyId, aProxyId, 'null')

        return await self.ExecQuery(
            'fmtUpd_Url.sql',
            {
                'aUrlId': aUrlId,
                'aUrlEn': aUrlEn,
                'aStatusCode': aStatusCode,
                'aProxyId': aProxyId
            }
        )

    async def InsHistUrl(self, aUrlId: int, aStatusCode: int, aParsedData: dict, aCrc: int, aUrlCount: int, aDataSize: int, aUserId: int) -> dict:
        if (aParsedData):
            ParsedData = json.dumps(aParsedData, indent=1, ensure_ascii=False)
        else:
            ParsedData = ''

        return await self.ExecQuery(
            'fmtIns_HistUrl.sql',
            {
                'aUrlId': aUrlId,
                'aStatusCode': aStatusCode,
                'aParsedData': ParsedData,
                'aCrc': aCrc,
                'aUrlCount': aUrlCount,
                'aDataSize': aDataSize,
                'aUserId': aUserId
            }
        )

    async def InsProduct(self, aUrlId: int, aParsedData: dict, aAttr: dict, aCrc: int) -> dict:
        ParsedData = json.dumps(aParsedData, indent=1, ensure_ascii=False)
        Attr = json.dumps(aAttr, indent=1, ensure_ascii=False)
        Title = aParsedData.get('name')[:128].replace("'", "''")

        return await self.ExecQuery(
            'fmtIns_Product.sql',
            {
                'aUrlId': aUrlId,
                'aTitle': Title,
                'aStock': aParsedData.get('stock', False),
                'aPrice': aParsedData.get('price')[0],
                'aParsedData': ParsedData,
                'aAttr': Attr,
                'aCrc': aCrc
            }
        )

    async def GetSiteCountry(self, aCountryId: int) -> dict:
        return await self.ExecQuery(
            'fmtGet_SiteCountry.sql',
            {
                'aCountryId': aCountryId
            }
        )

    async def GetSiteCountries(self, aLangId: int) -> dict:
        return await self.ExecQuery(
            'fmtGet_SiteCountries.sql',
            {
                'aLangId': aLangId
            }
        )

    async def GetCountryLangByName(self, aCountry: str) -> dict:
        return await self.ExecQuery(
            'fmtGet_CountryLangByName.sql',
            {
                'aCountry': aCountry
            }
        )

    async def GetCountryLangById(self, aCountryId: int) -> dict:
        return await self.ExecQuery(
            'fmtGet_CountryLangById.sql',
            {
                'aCountryId': aCountryId
            }
        )

    async def GetCountries(self, aLangId: int) -> dict:
        return await self.ExecQuery(
            'fmtGet_Countries.sql',
            {
                'aLangId': aLangId
            }
        )

    async def GetSiteInfo(self, aLangId: int, aSiteId: int) -> dict:
        return await self.ExecQuery(
            'fmtGet_SiteInfo.sql',
            {
                'aSiteId': aSiteId,
                'aLangId': aLangId
            }
        )
