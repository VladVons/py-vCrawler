# Created: 2025.01.04
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import time
from aiohttp import web
from aiohttp_session import get_session
#
from Inc.DbList import TDbList
from Inc.Misc.GeoIp import TGeoIp

class TSession():
    def __init__(self, aRequest: web.Request):
        self.Request = aRequest
        self.Session = None

    async def Init(self):
        self.Session = await get_session(self.Request)
        return self

    async def UpdateDb(self, aExec: callable):
        UserAgent = self.Request.headers.get('User-Agent', '')
        Remote = self.Request.remote
        if (Remote == '127.0.0.1'):
            # try to get remote ip from nginx proxy (proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;)
            Remote = self.Request.headers.get('X-FORWARDED-FOR', '127.0.0.1')

        Location = TGeoIp().GetCity(Remote)
        LocationArr = map(str, Location.values())
        LocationStr = ','.join(LocationArr).replace("'", '')

        Data = await aExec(
            'system',
            {
                'method': 'RegSession',
                'param' : {
                    'aIp': Remote,
                    'aUAgent': UserAgent.replace("'", '"'),
                    'aLocation': LocationStr
                }
            }
        )

        if ('err' not in Data):
            Dbl = TDbList().Import(Data)
            self.Set('session_id', Dbl.Rec.id)
            self.Set('start', int(time.time()))

    def Get(self, aKey: str) -> object:
        return self.Session.get(aKey)

    def GetAsDict(self) -> dict:
        return dict(self.Session)

    def GetId(self) -> int:
        return self.Get('session_id')

    def Set(self, aKey: str, aVal):
        self.Session[aKey] = aVal
