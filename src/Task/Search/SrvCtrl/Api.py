# Created: 2024.04.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
#
from Inc.Loader.Lang import TLoaderLangFs
from Inc.Var.Str import ToInt
from IncP.ApiBase import TApiBase
from IncP.Plugins import TCtrls

#import IncP.LibCtrl as Lib # recursion!
from Inc.DbList.DbList import TDbList
from Inc.Misc.Template import TDictRepl
from Inc.Var.Dict import GetDictDef, DictUpdate, DeepGet, DeepGetByList

class TDictReplDeep(TDictRepl):
    def _VarTpl(self):
        # example = 'this is a {{macros}}'
        self.ReVar = re.compile(r'(\{\{[a-zA-Z0-9_.]+\}\})')

    def _Get(self, aFind: str) -> str:
        aFind = aFind.strip('{}')
        Res = DeepGet(self.Dict, aFind)
        if (not isinstance(Res, (str, int, float))):
            Res = f'-{aFind}-'
        return Res


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
            Def = GetDictDef(Section, ['dir'], ['MVC/Search/lang'])
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
                'cache_age': -1
            }
        )
        Dbl = TDbList().Import(Data)
        return Dbl.Rec.val

    async def GetLang(self, aRoutes: list, aLangId: int) -> dict:
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
            DblLang = TDbList().Import(Data)
            self.Langs = DblLang.ExportPair('id', 'alias')

        Data = await self.ApiModel(
            'system',
            {
                'method': 'GetAliasLang',
                'param': {
                    'aLangId': aLangId
                },
                'cache_age': -1
            }
        )
        Res = Data['data'][0][0]

        Lang = self.Langs.get(aLangId, 'en')
        for xRoute in aRoutes:
            R = await self.Lang.Add(Lang, xRoute, 'tpl')
            Res.update(R)
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

    async def LoadLayout(self, aRoute: str, aLangId: int) -> dict:
        Data = await self.ApiModel(
            'system',
            {
                'method': 'GetLayoutLang',
                'param': {
                    'aLangId': aLangId,
                    'aRoute': aRoute
                },
                'cache_age': -1
            }
        )

        Dbl = TDbList().Import(Data)
        return Dbl

    async def Exec(self, aRoute: str, aData: dict) -> dict:
        self.ConfDb = await self.GetConfDb()

        Type = aData.get('type')
        match Type:
            case 'form':
                await super().Exec('system', aData | {'method': 'OnExec'})

                Res = {}
                # access Res from aData
                aData['res'] = Res

                Routes = aData.get('extends', [])
                Routes.append(aRoute)

                # language
                LangId = ToInt(DeepGetByList(aData, ['query', 'lang_id'], '1'))
                aData['query']['lang_id'] = ToInt(LangId)
                Res['lang'] = await self.GetLang(Routes, LangId)
                Res['lang_alias'] = self.Langs[LangId]

                # get misc page language. title, descr, meta etc
                Dbl = await self.LoadLayout(aRoute, LangId)
                DictUpdate(Res, Dbl.Rec.GetAsDict())

                for xRoute in Routes:
                    R = await super().Exec(xRoute, aData)
                    DictUpdate(Res, R)

                await self.SeoUrl(Res)

                # next exec chain if available
                if ('exec' in Res):
                    Exec = Res['exec']
                    R = await super().Exec(Exec.get('route', aRoute), aData | {'method': Exec['method']})
                    DictUpdate(Res, R)

                # serialize all dbl_.* keys
                for xKey, xVal in Res.items():
                    if (xKey.startswith('dbl_')) and (isinstance(xVal, TDbList)):
                        Res[xKey] = xVal.Export()

                DictRepl = TDictReplDeep(Res)
                DictRepl.InPlace(['title', 'meta_title', 'meta_descr'])
            case 'api':
                Res = await super().Exec(aRoute, aData)
                #Res = Encode(Res)
            case _:
                Res = {'err': f'unknown type {Type}'}
        return Res

ApiCtrl = TApiCtrl()
