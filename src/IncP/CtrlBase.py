# Created: 2023.05.14
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Misc.Cache import TCacheMem
from Inc.Misc.Profiler import TTimerLog
from Inc.Loader.Lang import TLoaderLang
from Task.Search.SrvCtrl.Api import TApiCtrl
import IncP.LibModel as Lib


class TCtrlBase():
    def __init__(self, aApiCtrl: TApiCtrl):
        self.ApiCtrl = aApiCtrl
        self.ApiModel = None
        self.ApiImg = None
        self.Cache = TCacheMem(aMaxAge = 30)

    def _init_(self):
        self.ApiModel = self.ApiCtrl.Loader['model'].Get
        #self.ApiImg = self.ApiCtrl.Loader['img'].Get

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
        Data = await self.ApiModel(aMethod, aData)
        DblData = Data.get('data')
        if (DblData):
            return Lib.TDbSql().Import(DblData)

