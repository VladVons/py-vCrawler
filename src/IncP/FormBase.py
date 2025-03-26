# Created: 2024.05.07
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from wtforms import Form
from aiohttp import web
from aiohttp.web_request import FileField
#
from Inc.Loader.Api import TLoaderApi
from Inc.Misc.Jinja import TTemplate
from Inc.Var.Dict import DeepGetByList
from Inc.Var.DictDef import TDictDef
from IncP import GetAppVer
from .Session import TSession


class TFormBase(Form):
    '''
        Base class for rendering string from templates
    '''

    def __init__(self, aParent, aRequest: web.Request):
        super().__init__()

        self.Parent = aParent
        self.Ctrl: TLoaderApi = aParent.Loader['ctrl']
        self.Request = aRequest
        self.Session = TSession(aRequest)
        self.Tpl: TTemplate = aParent.Tpl
        self.out = TDictDef(
            '',
            {
                'data': {},
                'files': [],
                'info': GetAppVer(),
                'title': '',
                'route': '',
                'path': '',
                'query': {}
            }
        )

        self._DoInit()

    def _DoInit(self):
        pass

    async def _DoRender(self):
        pass

    def _GetTplExtends(self, aRoute: str) -> list:
        File = self.Tpl.SearchModule(aRoute)
        if (File):
            Source = self.Tpl.Env.loader.LoadFile(File)
            Macro = self.Tpl.ReMacro.findall(Source)
            return [
                Val.replace('.j2', '')
                for Key, Val in Macro
                if Key == 'extends'
            ]

    async def ExecCtrlDef(self) -> dict:
        return await self.ExecCtrl(self.out.route, {'method': 'Main'})

    async def ExecCtrl(self, aRoute: str, aData: dict = None) -> dict:
        Data = {
            'type': 'form',
            'post': self.out.data,
            'query': dict(self.Request.query) | self.out.query,
            'path_qs': self.Request.path_qs,
            'user_agent': self.Request.headers.get('User-Agent', ''),
            'extends': self._GetTplExtends(aRoute),
            'session': self.Session.Export()
        }

        # debug view
        return await self.Ctrl.Get(aRoute, aData | Data)

    async def ExecCtrlApi(self, aRoute: str, aData: dict = None) -> dict:
        return await self.Ctrl.Get(aRoute, aData | {'type': 'api'})

    async def PostToData(self) -> bool:
        if (self.Request.method.lower() == 'post'):
            Post = await self.Request.post()
            self.process(Post)
            if (Post):
                for Key, Val in Post.items():
                    if (isinstance(Val, str)):
                        self.out.data[Key] = Val.strip()
                    elif (isinstance(Val, FileField)):
                        self.out.files.append((Val, Key))

                return bool(Post)

    async def Render(self) -> str:
        await self.Session.Init()
        if (not self.Session.GetId()):
            await self.Session.UpdateDb(self.ExecCtrlApi)

        await self.PostToData()
        Res = await self._DoRender()
        if (not Res):
            Res = self.RenderTemplate()
        return Res

    def RenderTemplate(self) -> str:
        File = f'{self.out.route}.{self.Tpl.Ext}'
        if ('status_code' in self.out):
            File = f'{self.Parent.Conf.form_info}.{self.Tpl.Ext}'
            ErrCode = f'status_code_{self.out.status_code}'
            self.out.info_data = DeepGetByList(self.out, ['lang',  ErrCode], 'Unknown error')
        return self.Tpl.Render(File, self.out)
