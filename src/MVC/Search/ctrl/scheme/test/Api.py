# Created: 2024.04.21
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
import json
from datetime import datetime
#
from Inc.DbList.DbUtil import TJsonEncoder
from Inc.Misc.Template import TDictRepl
from Inc.Scheme.Scheme import TScheme, TSchemeApi
from Inc.Scheme.Utils import FindLineInScheme
import IncP.LibCtrl as Lib
from . import Util


class TMain(Lib.TCtrlBase):
    async def Main(self, **aData: dict) -> dict:
        pass

    async def ScriptsLoad(self, aType: str) -> dict:
        async def _GetNew() -> dict:
            Dbl = await self.ExecModelImport(
                'scheme',
                {
                    'method': 'GetSchemeNew',
                    'param': {}
                }
            )

            if (Dbl):
                Format = {
                    '$date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                    '$url': Dbl.Rec.url
                }
                DictRepl = TDictRepl(Format)
                CurDir = __package__.replace('.', '/')

                DblRes = Lib.TDbList(['site_id', 'url_en', 'scheme'])
                for xName in ['product', 'category']:
                    DblRes.RecAdd([
                        Dbl.Rec.site_id,
                        xName,
                        DictRepl.ParseFile(f'{CurDir}/fmt_{xName}.json')
                    ])
                return DblRes.Export()

        async def _GetRnd() -> dict:
            return await self.ExecModel(
                'scheme',
                {
                    'method': 'GetSchemeRnd',
                    'param': {}
                }
            )

        async def _GetModerate() -> dict:
            return await self.ExecModel(
                'scheme',
                {
                    'method': 'GetSchemeModerate',
                    'param': {}
                }
            )

        match aType:
            case 'new':
                Res = await _GetNew()
            case 'rnd':
                Res = await _GetRnd()
            case 'moderate':
                Res = await _GetModerate()
            case _:
                Res = {}

        return {
            'dbl_script': Res
        }

    async def ScriptTest(self, aUrl: str, aScript: str, aEmul: bool) -> dict:
        Size = 0
        if (aUrl):
            UrlData = await Util.Cache.Download(aUrl, aEmul)
            if (UrlData['status'] != 200):
                return {'err': f'download code {UrlData["status"]}'}

            if (not aScript):
                Size = len(UrlData["data"]) // 1000
                return {'err': f'download ok. size: {Size}Kb'}
        else:
            return {'err': 'no url'}

        Script = Util.LoadScript(aScript)
        if ('err' in Script):
            return Script

        Type = list(Script.keys())[0]
        Script[Type]['info']['url'] = aUrl
        BSoup = Util.GetSoup(UrlData['data'])
        Scheme = TScheme(Script)
        Scheme.Parse(BSoup)
        Pipe = Scheme.GetPipe(Type)

        Checks = Util.CheckPipe(Pipe, Type)
        PipeStr = json.dumps(Pipe, indent=2, ensure_ascii=False, cls=TJsonEncoder)
        UniqErr = list(set(Scheme.Err))
        return {
            'err': '\n'.join(UniqErr + Checks),
            'data': PipeStr,
            'size': Size
        }

    async def ScriptSave(self, aSiteId: int, aName: str, aScript: str) -> dict:
        await self.ExecModel(
            'scheme',
            {
                'method': 'UpdScheme',
                'param': {
                    'aSiteId': aSiteId,
                    'aUrlEn': aName,
                    'aScheme': aScript
                }
            }
        )

    async def GetLineNo(self, aScript: str, aCurLine: str) -> dict:
        Res = {}
        if (re.search(r'\((none|unknown)\)$', aCurLine)):
            Path = aCurLine.split('->', maxsplit=1)[0]
            LineNo = FindLineInScheme(aScript, Path)
            Res = {
                'line': LineNo,
                'column': -1
            }
        elif (aCurLine.startswith('json:')):
            Match = re.search(r'line (\d+) column (\d+)', aCurLine)
            if (Match):
                Res = {
                    'line': int(Match.group(1)),
                    'column': int(Match.group(2))
                }
        return Res

    async def GetUrlFromText(self, aText: str) -> dict:
        Arr = re.findall(r'"(https?://[^\s]+)"', aText)
        if (Arr):
            return {'url': Arr[0]}

    async def GetHelp(self) -> dict:
        Help = TSchemeApi.help(None)
        return {'help': Help}

    async def GetPrettySrc(self, aUrl: str, aEmul: bool) -> dict:
        UrlData = await Util.Cache.Download(aUrl, aEmul)
        if (UrlData['status'] == 200):
            BSoup = Util.GetSoup(UrlData['data'])
            DataP = BSoup.prettify()
            Res = {'src': DataP}
        else:
            Res = {'err': f'download status code {UrlData["status"]}'}
        return Res

    async def GetMacroses(self, aScript: str) -> dict:
        R = Util.LoadScript(aScript)
        if ('err' in R):
            return R

        Macroses = Util.GetMacroses(R)
        PopularFirst = sorted(Macroses.items(), key=lambda item: f'{item[1]}{item[0]}')
        return {'macroses': PopularFirst}

    async def CacheClear(self) -> dict:
        FilesCnt = Util.Cache.GetSize()
        Util.Cache.Clear()
        return {'files_cnt': FilesCnt}

    async def ReserveTask(self, aUrl: str) -> dict:
        Dbl = await self.ExecModelImport(
            'scheme',
            {
                'method': 'UpdReserveTask',
                'param': {
                    'aUrl': aUrl,
                    'aHours': 24
                }
            }
        )
        UnlockDate = Dbl.Rec.unlock_date.strftime('%Y-%m-%d %H:%M')
        return {'unlock_date': UnlockDate}
