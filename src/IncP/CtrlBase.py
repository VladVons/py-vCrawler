# Created: 2024.04.03
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Misc.Profiler import TTimerLog
from Task.SrvCtrl.Api import TApiCtrl
import IncP.LibCtrl as Lib


class TCtrlBase():
    def __init__(self, aApiCtrl: TApiCtrl):
        self.ApiCtrl = aApiCtrl
        self.ApiModel = None

    def _init_(self):
        self.ApiModel = self.ApiCtrl.Loader['model'].Get

    @property
    def Name(self) -> str:
        return self.ApiCtrl.Name

    async def ExecModel(self, aMethod: str, aData: dict) -> dict:
        with TTimerLog('ApiModel', False, aFile = 'Timer'):
            Res = await self.ApiModel(aMethod, aData)
        return Res

    async def ExecModelImport(self, aMethod: str, aData: dict) -> dict:
        Data = await self.ApiModel(aMethod, aData)
        if (Data):
            return Lib.TDbSql().Import(Data)

    async def ExecModelExport(self, aMethod: str, aData: dict) -> dict:
        Dbl = await self.ExecModelImport(aMethod, aData)
        if (Dbl):
            return Dbl.Export()

    async def ExecSelf(self, aRoute: str, aData: dict) -> dict:
        return await self.ApiCtrl.Exec(aRoute, aData)
