# Created: 2024.04.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Sql.DbModel import TDbModel
import IncP.LibModel as Lib


class TMain(TDbModel):
    async def GetSiteExt(self, aSiteId: int) -> dict:
        return await self.ExecQuery(
            'fmtGet_SiteExt.sql',
            {'aSiteId': aSiteId}
        )

    @Lib.DTransaction
    async def _DtGet_SiteUrlToUpdate(self, aData: dict, aCursor = None) -> dict:
        aLimit = aData.get('aLimit')

        DblData = await self.ExecQueryCursor(
            'fmtGet_UrlToUpdate.sql',
            {'aLimit': aLimit},
            aCursor
        )

        Dbl = Lib.TDbList().Import(DblData)
        if (Dbl):
            UrlIds = Dbl.ExportList('url_id')
            UrlIds = Lib.ListIntToComma(UrlIds)
            await self.ExecQuery(
                'fmtUpd_SiteUrlToUpdateUnlock.sql',
                {'aSiteId': Dbl.Rec.site_id, 'UrlIds': UrlIds, 'aLimit': aLimit}
            )
        return DblData

    async def GetUrlToUpdate(self) -> dict:
        return await self.ExecQuery(
            'fmtGet_UrlToUpdate.sql',
            {}
        )

    async def GetSiteUrlToUpdate(self, aLimit: int) -> dict:
        return await self._DtGet_SiteUrlToUpdate(locals())
