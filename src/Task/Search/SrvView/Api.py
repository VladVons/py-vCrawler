# Created: 2024.05.07
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import json
from aiohttp import web
#
from Inc.DataClass import DDataClass
from Inc.Misc.Jinja import TTemplate
from IncP.ApiBase import TApiBase
from IncP.FormBase import TFormBase
from IncP.Log import Log
from IncP.Plugins import TViewes
from IncP.Session import TSession



class TFormRender(TFormBase):
    async def _DoRender(self):
        Data = await self.ExecCtrlDef()
        if (Data):
            self.out.update(Data)


@DDataClass
class TApiViewConf():
    loader: dict
    cache_route: dict = {}
    ip_log: dict = {}
    dir_route: str = 'MVC/view'
    dir_root: str = 'MVC/view'
    form_home: str = 'common/home'
    form_info: str = 'common/info'
    request_scheme: str = 'http'


class TApiView(TApiBase):
    def __init__(self):
        super().__init__()

        Conf = self.GetConf()
        self.Conf = TApiViewConf(**Conf)
        self.Viewes = TViewes(self.Conf.dir_route)
        self.InitLoader(self.Conf.loader)
        self.Tpl = TTemplate([f'{self.Conf.dir_root}/tpl'])

    def GetForm(self, aRequest: web.Request, aRoute: str) -> TFormBase:
        if (aRoute.startswith('/')):
            return

        TplFile = self.Tpl.SearchModule(aRoute)
        if (not TplFile):
            return

        Locate = [
            (TplFile.rsplit('.', maxsplit=1)[0], 'TForm')
        ]

        for Module, Class in Locate:
            try:
                if (os.path.isfile(Module + '.py')):
                    Mod = __import__(Module.replace('/', '.'), None, None, [Class])
                    TClass = getattr(Mod, Class)
                    return TClass(self, aRequest)
            except ModuleNotFoundError:
                pass
        return TFormRender(self, aRequest)
        #raise ModuleNotFoundError(Locate[-1])

    async def GetFormData(self, aRequest: web.Request, aQuery: dict) -> dict:
        Route = aQuery['route']
        Form = self.GetForm(aRequest, Route)
        if (Form):
            Form.out.route = Route
            Form.out.path = self.Name
            Form.out.query = aQuery
            Data = await Form.Render()
            Res = {
                'data': Data,
                'status_code': Form.out.get('status_code', 200),
                'status_value': Form.out.get('status_value'),
            }
        else:
            Res = {
                'err': f'Route not found {Route}',
                'status_code': 404
            }
        return Res

    async def ResponseForm(self, aRequest: web.Request, aQuery: dict) -> web.Response:
        Data = await self.GetFormData(aRequest, aQuery)
        if ('err' in Data):
            if (Data['status_code'] in [301, 302]):
                raise web.HTTPFound(location = Data['status_value'])
            Res = await self.ResponseFormInfo(aRequest, Data['err'], Data['status_code'])
        else:
            Res = web.Response(text = Data['data'], content_type = 'text/html', status = Data['status_code'])
        return Res

    async def ResponseFormInfo(self, aRequest: web.Request, aText: str, aStatus: int = 200) -> web.Response:
        if (self.Tpl.SearchModule(self.Conf.form_info)):
            Res = await self.ResponseForm(aRequest, {'route': self.Conf.form_info, 'info': aText})
        else:
            Text = f'1) {aText}.\n2) Info template {self.Conf.form_info} not found'
            Res = web.Response(text = Text, content_type = 'text/html', status = aStatus)
        Res.set_status(aStatus, aText)
        return Res

    async def ResponseApi(self, aRequest: web.Request) -> web.Response:
        Session = TSession(aRequest)
        await Session.Init()

        Query = dict(aRequest.query)
        Post = await aRequest.post()
        Data = {
            'type': 'api',
            'method': Query.get('method', 'Main'),
            'post': dict(Post),
            'query': dict(aRequest.query),
            'session': Session.Export(),
            'path_qs': aRequest.path_qs
        }

        Post = await aRequest.text()
        if (Post):
            try:
                Post = json.loads(Post)
                Data.update(Post)
            except ValueError as E:
                Log.Print(1, 'i', f'ResponseApi(). {E}')

        Ctrl = self.Loader['ctrl']
        R = await Ctrl.Get(Query.get('route'), Data)

        Context = Query.get('context', 'json')
        if (Context == 'json') and (R is not None):
            Res = web.json_response(data = R)
        else:
            Res = web.Response(text = R)
        return Res

    async def GetSeoUrl(self, aMethod: str, aUrl: str) -> str:
        Data = {
            'type': 'api',
            'method': aMethod,
            'param': {
                'aPath': aUrl
            }
        }
        Ctrl = self.Loader['ctrl']
        return await Ctrl.Get('seo', Data)

ApiView = TApiView()
