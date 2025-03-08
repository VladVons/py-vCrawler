# Created: 2025.01.04
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import time
from aiohttp import web
from aiohttp_session import get_session
#
from Inc.DbList import TDbList
from Inc.Misc.GeoIp import TGeoIp


def GetIpLocation(aRequest: web.Request) -> dict:
    Remote = aRequest.remote
    LocalHost = '127.0.0.1'
    if (Remote == LocalHost):
        # try to get remote ip from nginx proxy (proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;)
        #Remote = '5.58.222.201'
        Remote = aRequest.headers.get('X-FORWARDED-FOR', Remote)

    if (Remote == LocalHost):
        Location = {}
    else:
        Location = TGeoIp().GetCity(Remote)

    return {'ip': Remote, 'location': Location}

class TSession():
    def __init__(self, aRequest: web.Request):
        self.Request = aRequest
        self.Session = None
        self.Remote, self.Location = GetIpLocation(self.Request).values()

    async def Init(self):
        self.Session = await get_session(self.Request)
        return self

    async def UpdateDb(self, aExec: callable):
        UserAgent = self.Request.headers.get('User-Agent', '')
        LocationArr = map(str, self.Location.values())
        LocationStr = ','.join(LocationArr).replace("'", '')

        Data = await aExec(
            'system',
            {
                'method': 'RegSession',
                'param' : {
                    'aIp': self.Remote,
                    'aUAgent': UserAgent.replace("'", '"'),
                    'aLocation': LocationStr
                }
            }
        )

        if ('err' not in Data):
            Dbl = TDbList().Import(Data)
            self.Set('session_id', Dbl.Rec.id)
            self.Set('start', int(time.time()))


    def Export(self) -> dict:
        Res = {
            'keys': self.GetAsDict(),
            'ip': self.Remote,
            'location': self.Location,
            'cookies': dict(self.Request.cookies)
        }
        return Res

    def Get(self, aKey: str) -> object:
        return self.Session.get(aKey)

    def GetAsDict(self) -> dict:
        return dict(self.Session)

    def GetId(self) -> int:
        return self.Get('session_id')

    def Set(self, aKey: str, aVal):
        self.Session[aKey] = aVal
