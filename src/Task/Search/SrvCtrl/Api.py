# Created: 2024.04.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Loader.Lang import TLoaderLangFs
from Inc.Misc.Serialize import Encode
from Inc.Var.Str import ToInt
from IncP.ApiBase import TApiBase
from IncP.Plugins import TCtrls
import IncP.LibModel as Lib


class TApiCtrl(TApiBase):
    def __init__(self):
        super().__init__()

        Conf = self.GetConf()

        self.Plugin = TCtrls(Conf['dir_route'], self)

        self.InitLoader(Conf['loader'])
        self.ApiModel = self.Loader['model'].Get

        self.Langs = {}
        Section = Conf['lang']
        if (Section['type'] == 'fs'):
            Def = Lib.GetDictDef(Section, ['dir'], ['MVC/Search/lang'])
            self.Lang = TLoaderLangFs(*Def)
        else:
            raise ValueError()

    async def GetLang(self, aLangId: int, aRoutes: list) -> dict:
        if (not self.Langs):
            Data = await self.ApiModel(
                'system',
                {
                    'method': 'GetLang',
                    'param': {
                        'aLangId': 1
                    }
                }
            )
            DblLang = Lib.TDbList().Import(Data)
            self.Langs = DblLang.ExportPair('id', 'alias')

        Data = await self.ApiModel(
            'system',
            {
                'method': 'GetAliasLang',
                'param': {
                    'aLangId': aLangId
                },
                'cache_age': 60*10
            }
        )
        Res = Data['data'][0][0]

        Lang = self.Langs.get(aLangId, 'en')
        for xRoute in aRoutes:
            await self.Lang.Add(Lang, xRoute, 'tpl')
        Res.update(self.Lang.Join())
        return Res

    async def Exec(self, aRoute: str, aData: dict) -> dict:
        Type = aData.get('type')
        match Type:
            case 'form':
                Res = {}
                Routes = aData.get('extends', [])
                Routes.append(aRoute)

                LangId = Lib.DeepGetByList(aData, ['query', 'lang_id'], '1')
                LangId = ToInt(LangId, 1)
                Res['lang'] = await self.GetLang(LangId, Routes)

                aData['res'] = Res
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
