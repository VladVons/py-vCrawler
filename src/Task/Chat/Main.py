# Created: 2025.04.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from aiohttp import web
#
from Inc.SrvWeb import TSrvBase
from IncP.Log import Log
from .Api import ApiChat


class TSrvChat(TSrvBase):
    def _GetDefRoutes(self) -> list:
        return [
            web.get('/ws', ApiChat.Handle)
        ]

    async def RunApp(self):
        Log.Print(1, 'i', f'{self.__class__.__name__}.RunApp() on port {self._SrvConf.port}')

        await ApiChat.InitA()
        App = self.CreateApp()
        await self.Run(App)
