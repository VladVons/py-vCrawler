# Created: 2025.01.06
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibModel as Lib

class TMain(Lib.TDbModel):
    async def InsMail(self, aMail: str, aSubject: str, aBody: str, aInboxEn: str, aIp: str = None) -> dict:
        return await self.ExecQuery(
            'fmtIns_Mail.sql',
            {
                'aMail': aMail,
                'aSubject': aSubject,
                'aBody': aBody,
                'aIp': aIp,
                'aInboxEn': aInboxEn
            }
        )
