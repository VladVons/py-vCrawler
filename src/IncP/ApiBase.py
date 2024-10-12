# Created: 2023.02.02
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Loader.Api import TLoaderApiFs, TLoaderApiHttp
from Inc.Plugin import TPlugin
from Inc.Var.Dict import DictToText
from Inc.Util.ModHelp import GetHelp, GetMethod
from IncP.Plugins import TPluginMVC
from IncP.Log import Log
from Task import App


class TApiBase():
    def __init__(self):
        self.ExecCnt = 0
        self.Loader = {}
        self.AEvent = None
        self.Name = None
        self.DefRoute = None
        self.Plugin: TPluginMVC = None

    async def ExecOnce(self, aData: dict):
        pass

    @staticmethod
    def _GetMethodHelp(aMod: object, aMethod: str) -> dict:
        Obj = getattr(aMod, aMethod, None)
        if (Obj is None):
            Res = {
                'err': f'unknown method {aMethod}',
                'help': GetHelp(aMod)
            }
        else:
            Data = GetMethod(Obj)
            Res = {
                'help': {'decl': Data[2],
                'doc': Data[3]}
            }
        return Res

    def GetConf(self) -> dict:
        return App.LoadClassConf(self)

    def GetMethod(self, aPlugin: TPlugin, aRoute: str, aData: dict) -> dict:
        Method = aData.get('method')

        Key = f'{aRoute}/{Method}'
        Res = aPlugin.Cache.get(Key)
        if (not Res):
            if (not Method):
                return {'err': 'undefined key `method`'}

            if (not aPlugin.IsModule(aRoute)):
                if (self.DefRoute):
                    aRoute = self.DefRoute
                else:
                    return {'err': f'Route not found {aRoute}', 'status_code': 404}

            aPlugin.LoadMod(aRoute)
            RouteObj = aPlugin[aRoute]

            MethodObj = getattr(RouteObj, Method, None)
            if (MethodObj is None):
                return {'err': f'Method {Method} not found in route {aRoute}', 'status_code': 404}

            Res = {'method': MethodObj, 'module': RouteObj}
            aPlugin.Cache[Key] = Res
        return Res

    async def Exec(self, aRoute: str, aData: dict) -> dict:
        Log.Print(3, 'i', f'{self.__class__.__name__}.Exec(). route: {aRoute}; {DictToText(aData, ', ')}')

        if (self.ExecCnt == 0):
            await self.ExecOnce(aData)
        self.ExecCnt += 1

        Res = self.GetMethod(self.Plugin, aRoute, aData)
        if ('err' not in Res):
            Param = aData.get('param', {})
            Method = Res['method']
            #Args = Method.__code__.co_varnames[:Method.__code__.co_argcount]
            try:
                Res = await Method(**Param)
            except TypeError as E:
                Log.Print(1, 'x', 'Exec()', aE = E)
                Res = {'err': E}
        return Res

    def InitLoader(self, aConf: dict):
        for Key, Val in aConf.items():
            if (not Key.startswith('-')):
                Type = Val['type']
                match Type:
                    case 'url':
                        Loader = TLoaderApiHttp(Val['user'], Val['password'], Val['url'])
                    case 'fs':
                        Loader = TLoaderApiFs(Val['module'], Val['class'], self.Name)
                    case _:
                        raise ValueError(f'unknown type {Type}')
                self.Loader[Key] = Loader
