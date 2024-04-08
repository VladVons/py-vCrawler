# Created: 2024.04.06
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import asyncio
from IncP.CtrlBase import TCtrlBase, Lib

Lock = asyncio.Lock()

class TMain(TCtrlBase):
    async def GetSiteUrlToUpdate(self) -> dict:
        async with Lock:
            DataSite = await self.ExecModel(
                'site',
                {
                    'method': 'GetSiteToUpdate'
                }
            )

            Res = {}
            Res['site'] = DataSite

            DblSite = Lib.TDbList().Import(DataSite)
            if (DblSite):
                MaxUrls = DblSite.Rec.urls_parse
                DataUrl = await self.ExecModel(
                    'site',
                    {
                        'method': 'GetUrlToUpdate',
                        'param': {
                            'aSiteId': DblSite.Rec.id,
                            'aLimit': MaxUrls
                        }
                    }
                )
                Res['url'] = DataUrl

                Reserv = MaxUrls // int(100/20)
                DblUrl = Lib.TDbList().Import(DataUrl)
                await self.ExecModel(
                    'site',
                    {
                        'method': 'SetUrlToUpdateLock',
                        'param': {
                            'aSiteId': DblSite.Rec.id,
                            'aUrlIds': DblUrl.ExportList('url_id'),
                            'aLimit': MaxUrls + Reserv
                        }
                    }
                )
            return Res
