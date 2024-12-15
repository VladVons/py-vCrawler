# Created: 2023.05.14
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Misc.Profiler import TTimerLog
from Inc.Loader.Lang import TLoaderLang
from Task.Search.SrvCtrl.Api import TApiCtrl
import IncP.LibCtrl as Lib


class TCtrlBase():
    def __init__(self, aApiCtrl: TApiCtrl):
        self.ApiCtrl = aApiCtrl
        self.ApiModel = None
        self.ApiImg = None


    def _init_(self):
        self.ApiModel = self.ApiCtrl.Loader['model'].Get
        #self.ApiImg = self.ApiCtrl.Loader['img'].Get
        pass

    @property
    def Common(self) -> TApiCtrl:
        return self.ApiCtrl.ApiCommon.Ctrls.ApiCtrl

    @property
    def Lang(self) -> TLoaderLang:
        return self.ApiCtrl.Lang

    @property
    def Name(self) -> str:
        return self.ApiCtrl.Name

    async def ExecModel(self, aMethod: str, aData: dict) -> dict:
        #Res = await self.ApiCtrl.CacheModel.ProxyA(aMethod, aData, self.ApiModel, [aMethod, aData])
        with TTimerLog('ApiModel', False, aFile = 'Timer'):
            Res = await self.ApiModel(aMethod, aData)
        return Res

    async def ExecModelImport(self, aMethod: str, aData: dict) -> dict:
        Res = await self.ApiModel(aMethod, aData)
        if (isinstance(Res, dict) and ('tag' in Res) and ('head' in Res)):
            Res = Lib.TDbList().Import(Res)
        return Res

    async def Translate(self, aLang: str, aText: list[str]) -> dict:
        Data = await self.ExecModel(
            'system',
            {
                'method': 'GetAliasTranslate',
                'param': {
                    'aLang': aLang,
                    'aText': aText
                }
            }
        )
        return Data['data'][0][0]
