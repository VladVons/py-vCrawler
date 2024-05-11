# Created: 2024.05.07
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import re
from aiohttp import web
#
from Inc.DataClass import DDataClass
from Inc.SrvWeb import TSrvBase, TSrvConf
from IncP.Log import Log
from .Api import ApiView, TApiView


@DDataClass
class TSrvViewConf(TSrvConf):
    deny: str = r'.j2$|.py$'

class TSrvView(TSrvBase):
    ''' web server for end user'''

    def __init__(self, aSrvConf: TSrvViewConf):
        super().__init__(aSrvConf)
        self._SrvConf = aSrvConf

    def _GetDefRoutes(self) -> list:
        return [
            web.get('/{name:.*}', self._rIndex),
            web.post('/{name:.*}', self._rIndex)
        ]

    async def _LoadFile(self, aRequest: web.Request, aApiView: TApiView) -> web.Response:
        Name = aRequest.match_info.get('name')
        File = f'{aApiView.Conf.dir_root}/{Name}'
        if (os.path.isfile(File)):
            if (re.search(self._SrvConf.deny, Name)):
                Res = await aApiView.ResponseFormInfo(aRequest, f'Access denied {aRequest.path}', 403)
            else:
                Res = self._GetMimeFile(File)
        else:
            Res = await self._Err_404(aRequest)
        return Res

    @staticmethod
    async def _Err_404(aRequest: web.Request) -> web.Response:
        Path = aRequest.match_info.get('name')
        return await ApiView.ResponseFormInfo(aRequest, f'Path not found {Path}', 404)

    @staticmethod
    async def _Err_All(_aRequest: web.Request, aStack: dict) -> web.Response:
        Data = '\n<br>'.join(aStack)
        return web.Response(text = Data, content_type = 'text/html', status = 500)

    async def _rIndex(self, aRequest: web.Request) -> web.Response:
        if (aRequest.path == '/'):
            Query = dict(aRequest.query)
            if ('route' not in aRequest.query):
                Query['route'] = ApiView.Conf.form_home
            Res = await ApiView.ResponseForm(aRequest, Query)
        else:
            Res = await self._LoadFile(aRequest, ApiView)
        return Res

    async def RunApp(self):
        Log.Print(1, 'i', f'{self.__class__.__name__}.RunApp() on port {self._SrvConf.port}')

        ErroMiddleware = {404: self._Err_404, 'err_all': self._Err_All}
        App = self.CreateApp(aErroMiddleware = ErroMiddleware)
        await self.Run(App)
