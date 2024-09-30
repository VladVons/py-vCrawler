# Created: 2024.04.07
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Var.Str import ToObj
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

        if (isinstance(Dbl, Lib.TDbList)):
            if (Dbl.GetSize() > 0):
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

                Res = {Rec.attr: ToObj(Rec.val) for Rec in Dbl}
                Res['user_id'] = UserId
                return Res
        else:
            Lib.Log.Print(1, 'i', f'GetUserExt(). {Dbl.get('err')}')
