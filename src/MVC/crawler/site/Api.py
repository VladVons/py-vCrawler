# Created: 2024.04.07
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.CrawlerBase import TCrawlerBase


class TMain(TCrawlerBase):
    async def GetSiteUrlToUpdate(self):
        return await self.ExecCtrl(
            'site',
            {
                'method': 'GetSiteUrlToUpdate',
                'param': {
                    'aLimit': 10
                }
            }
        )
