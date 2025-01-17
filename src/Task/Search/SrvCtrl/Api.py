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

        self.ConfDb = {}

        self.Langs = {}
        Section = Conf['lang']
        if (Section['type'] == 'fs'):
            Def = Lib.GetDictDef(Section, ['dir'], ['MVC/Search/lang'])
            self.Lang = TLoaderLangFs(*Def)
        else:
            raise ValueError()

    async def GetConfDb(self) -> dict:
        Data = await self.ApiModel(
            'system',
            {
                'method': 'GetConf',
                'param': {
                    'aAttr': None
                },
                'cache_age': 60*1
            }
        )
        Dbl = Lib.TDbList().Import(Data)
        return Dbl.Rec.val

    async def GetLang(self, aRoutes: list, aData: dict) -> dict:
        aLangId, aCountryId = Lib.GetDictDefs(
            aData.get('query'),
            ('lang_id', 'country_id'),
            (1, -1)
        )

        if (aCountryId == -1):
            Country = Lib.DeepGetByList(aData, ['session', 'location', 'country'])
            #Country = 'Ukraine'
            if (Country):
                Data = await self.ApiModel(
                    'site',
                    {
                        'method': 'GetCountryLang',
                        'param': {
                            'aCountry': Country.strip()
                        }
                    }
                )
                Dbl = Lib.TDbList().Import(Data)
                if (Dbl):
                    aLangId = aData['query']['lang_id'] = Dbl.Rec.lang_id
                    aData['query']['country_id'] = Dbl.Rec.country_id

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

    async def SeoEncodeList(self, aPaths: list[str]) -> list[str]:
        if (aPaths):
            return await self.ApiModel(
                'seo',
                {
                    'type': 'api',
                    'method': 'Encode',
                    'param': {
                        'aPath': aPaths
                    }
                }
            )

    async def SeoUrl(self, aRes: dict):
        if ('href' in aRes) and (self.ConfDb.get('seo_url')):
            Href = aRes['href']
            Seo = await super().Exec(
                'seo',
                {
                    'method': 'Encode',
                    'param': {
                        'aPath': Href.values()
                    }
                }
            )
            aRes['href'] = dict(zip(Href.keys(), Seo))

    async def Exec(self, aRoute: str, aData: dict) -> dict:
        self.ConfDb = await self.GetConfDb()

        Type = aData.get('type')
        match Type:
            case 'form':
                await super().Exec('system', aData | {'method': 'OnExec'})

                Res = {}
                Routes = aData.get('extends', [])
                Routes.append(aRoute)

                Res['lang'] = await self.GetLang(Routes, aData)

                aData['res'] = Res
                for xRoute in Routes:
                    R = await super().Exec(xRoute, aData)
                    Lib.DictUpdate(Res, R)
                await self.SeoUrl(Res)
            case 'api':
                Res = await super().Exec(aRoute, aData)
                #Res = Encode(Res)
            case _:
                Res = {'err': f'unknown type {Type}'}
        return Res

ApiCtrl = TApiCtrl()
