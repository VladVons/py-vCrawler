# Created: 2024.04.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Sql.DbModel import TDbModel
import IncP.LibModel as Lib


class TMain(TDbModel):
    @Lib.DTransaction
    async def _Get_SiteUrlToUpdate(self, aData: dict, aCursor = None) -> dict:
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

    async def Get_UrlToUpdate(self) -> dict:
        return await self.ExecQuery(
            'fmtGet_UrlToUpdate.sql',
            {}
        )

    async def Get_SiteUrlToUpdate(self, aLimit: int) -> dict:
        Res = await self._Get_SiteUrlToUpdate(locals())
        return Res
