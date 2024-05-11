# Created: 2024.04.09
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Task.Collector.SrvModel.Api import TApiModel
import IncP.LibCrawler as Lib


class TModelBase():
    def __init__(self, aApiModel: TApiModel, _Path: str):
        self.ApiModel = aApiModel

    async def Exec(self, aMethod: str, aData: dict) -> dict:
        Res = await self.ApiModel.Exec(aMethod, aData)
        if (isinstance(Res, dict) and ('tag' in Res)):
            Res = Lib.TDbList().Import(Res)
        return Res
