# Created: 2024.04.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Loader.Lang import TLoaderLangFs
from Inc.Misc.Serialize import Encode
from IncP.ApiBase import TApiBase
from IncP.Plugins import TCtrls
import IncP.LibModel as Lib


class TApiCtrl(TApiBase):
    def __init__(self):
        super().__init__()

        Conf = self.GetConf()

        self.Plugin = TCtrls(Conf['dir_route'], self)
        self.InitLoader(Conf['loader'])

        Section = Conf['lang']
        if (Section['type'] == 'fs'):
            Def = Lib.GetDictDef(Section, ['dir'], ['MVC/Search/lang'])
            self.Lang = TLoaderLangFs(*Def)
        else:
            raise ValueError()

    async def Exec(self, aRoute: str, aData: dict) -> dict:
        Type = aData.get('type')
        match Type:
            case 'form':
                Routes = aData.get('extends', [])
                Routes.append(aRoute)
                for xRoute in Routes:
                    await self.Lang.Add('en', xRoute, 'tpl')
                Lang = self.Lang.Join()
                Res = {'lang': Lang}

                for xRoute in Routes:
                    ResExec = await super().Exec(xRoute, aData)
                    if (isinstance(ResExec, dict)):
                        Res.update(ResExec)
            case 'api':
                Res = await super().Exec(aRoute, aData)
                #Res = Encode(Res)
            case _:
                Res = {'err': f'unknown type {Type}'}
        return Res

ApiCtrl = TApiCtrl()
