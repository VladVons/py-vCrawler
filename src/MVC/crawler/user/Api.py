# Created: 2024.04.07
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.CrawlerBase import TCrawlerBase
import IncP.LibCrawler as Lib


class TMain(TCrawlerBase):
    async def GetUserExt(self, aLogin: str, aPassw: str):
        Dbl = await self.ExecModel(
            'user',
            {
                'method': 'GetUserId',
                'param': {
                   'aLogin': aLogin,
                   'aPassw': aPassw,
                }
            }
        )

        if (isinstance(Dbl, Lib.TDbList)) and (Dbl):
            UserId = Dbl.Rec.id
            Dbl = await self.ExecModel(
                'user',
                {
                    'method': 'GetUserExt',
                    'param': {
                        'aUserId': UserId
                    }
                }
            )
            Res = Dbl.ExportPair('attr', 'val')
            Res['user_id'] = UserId
            return Res
