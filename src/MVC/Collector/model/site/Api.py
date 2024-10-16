# Created: 2024.04.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import asyncio
import json
#
from Inc.Sql.DbModel import TDbModel
import IncP.LibModel as Lib

Lock = asyncio.Lock()


class TMain(TDbModel):
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
        await self.ExecQuery(
            'fmtIns_Urls.sql',
            {
                'aValues': ', '.join(Arr)
            }
        )

    async def UpdUrl(self, aUrlId: int, aUrlEn: str, aStatusCode: int) -> dict:
        return await self.ExecQuery(
            'fmtUpd_Url.sql',
            {
                'aUrlId': aUrlId,
                'aUrlEn': aUrlEn,
                'aStatusCode': aStatusCode
            }
        )

    async def InsHistUrl(self, aUrlId: int, aStatusCode: int, aParsedData: dict, aUrlCount: int, aDataSize: int, aUserId: int) -> dict:
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
                'aUrlCount': aUrlCount,
                'aDataSize': aDataSize,
                'aUserId': aUserId
            }
        )
