# Created: 2024.04.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import asyncio
#
from Inc.ParserSpec.LibsComp import TLibsComp
from IncP.Common import AdjustAttr
from IncP.ModelBase import TModelBase, Lib

Lock = asyncio.Lock()

class TMain(TModelBase):
    async def GetTask(self, aUserId: int) -> dict:
        async with Lock:
            DblSite = await self.Exec(
                'site',
                {
                    'method': 'GetSiteToUpdate',
                    'param': {}
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
                    if (DblUrl.Rec.url_id):
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
                    else:
                        Msg = f'no record in ref_url for {DblSite.Rec.url}'
                        Res['err'] = Msg
                        Lib.Log.Print(1, 'i', Msg)
            return Res

    async def InsUrls(self, aSiteId: int, aUrls: list[str]) -> dict:
        Res = await self.Exec(
            'site',
            {
                'method': 'InsUrls',
                'param': {
                    'aSiteId': aSiteId,
                    'aUrls': aUrls
                }
            }
        )

        # Res = await self.Exec(
        #     'site',
        #     {
        #         'method': 'GetUrlToUpdate_FromList',
        #         'param': {
        #             'aSiteId': aSiteId,
        #             'aUrls': aUrls
        #         }
        #     }
        # )
        return Res

    async def UpdUrl(self, aUrlId: int, aStatusCode: int, aUrlEn: str = None) -> dict:
        await self.Exec(
            'site',
            {
                'method': 'UpdUrl',
                'param': {
                    'aUrlId': aUrlId,
                    'aUrlEn': aUrlEn,
                    'aStatusCode': aStatusCode
                }
            }
        )

    async def InsUrlData(self, aUrlId: int, aStatusCode: int, aParsedData: dict, aCrc: int, aUrlCount: int = 0, aDataSize: int = 0, aUserId: int = 1, aUrlEn: str = None) -> dict:
        if (aUrlEn == 'product'):
            Title = aParsedData.get('name')
            LibsComp = TLibsComp()
            Attr = LibsComp.Parse(Title)
            AttrPath = AdjustAttr(Attr)

            await self.Exec(
                'site',
                {
                    'method': 'InsProduct',
                    'param': {
                        'aUrlId': aUrlId,
                        'aParsedData': aParsedData,
                        'aAttr': AttrPath,
                        'aCrc': aCrc
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
                    'aCrc': aCrc,
                    'aUrlCount': aUrlCount,
                    'aDataSize': aDataSize,
                    'aUserId': aUserId
                }
            }
        )
