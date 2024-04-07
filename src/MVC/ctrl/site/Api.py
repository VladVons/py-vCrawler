# Created: 2024.04.06
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.CtrlBase import TCtrlBase, Lib


class TMain(TCtrlBase):
    async def GetSiteUrlToUpdate(self, aLimit: int) -> dict:
        DblUrls = await self.ExecModelImport(
            'site',
            {
                'method': 'GetSiteUrlToUpdate',
                'param': {
                   'aLimit': aLimit
                }
            }
        )

        if (DblUrls):
            DblSite = await self.ExecModelImport(
                'site',
                {
                    'method': 'GetSiteInfo',
                    'param': {
                        'aSiteId': DblUrls.Rec.site_id
                    }
                }
            )

            return {
                'urls': DblUrls.Export(),
                'conf': ''
            }
