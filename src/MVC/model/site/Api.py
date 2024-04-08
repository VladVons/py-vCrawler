# Created: 2024.04.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Sql.DbModel import TDbModel
import IncP.LibModel as Lib


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
