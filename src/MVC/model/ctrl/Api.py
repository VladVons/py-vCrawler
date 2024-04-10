# Created: 2024.04.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import asyncio
#
from IncP.ModelBase import TModelBase, Lib

Lock = asyncio.Lock()

class TMain(TModelBase):
    async def GetSiteUrlToUpdate(self, aUserId: int) -> dict:
        async with Lock:
            DblSite = await self.Exec(
                'site',
                {
                    'method': 'GetSiteToUpdate'
                }
            )

            Res = {
                'site': DblSite.Export(),
                'url': None
            }

            if (DblSite):
                MaxUrls = DblSite.Rec.urls_parse
                DblUrl = await self.Exec(
                    'site',
                    {
                        'method': 'GetUrlToUpdate',
                        'param': {
                            'aSiteId': DblSite.Rec.id,
                            'aLimit': MaxUrls
                        }
                    }
                )

                if (DblUrl):
                    Res['url'] = DblUrl.Export()

                    Len = len(DblUrl)
                    Reserv = Len // int(100/20)
                    await self.Exec(
                        'site',
                        {
                            'method': 'SetUrlToUpdateLock',
                            'param': {
                                'aSiteId': DblSite.Rec.id,
                                'aUrlIds': DblUrl.ExportList('url_id'),
                                'aLimit': Len + Reserv
                            }
                        }
                    )
            return Res

    async def InsUrls(self, aSiteId: int, aUrls: list[str]) -> dict:
        await self.Exec(
            'site',
            {
                'method': 'InsUrls',
                'param': {
                    'aSiteId': aSiteId,
                    'aUrls': aUrls
                }
            }
        )

        return await self.Exec(
            'site',
            {
                'method': 'GetUrlToUpdate_FromList',
                'param': {
                    'aSiteId': aSiteId,
                    'aUrls': aUrls
                }
            }
        )

    async def InsHistUrl(self, aUrlId: int, aStatusCode: int, aParsedData: dict = None, aUrlCount: int = 0, aDataSize: int = 0, aUserId: int = 1) -> dict:
        await self.Exec(
            'site',
            {
                'method': 'UpdUrl',
                'param': {
                    'aUrlId': aUrlId,
                    'aUrlEn': Lib.Iif(aParsedData, 'product', None)
                }
            }
        )

        await self.Exec(
            'site',
            {
                'method': 'InsHistUrl',
                'param': {
                    'aUrlId': aUrlId,
                    'aStatusCode': aStatusCode,
                    'aParsedData': aParsedData,
                    'aUrlCount': aUrlCount,
                    'aDataSize': aDataSize,
                    'aUserId': aUserId
                }
            }
        )
