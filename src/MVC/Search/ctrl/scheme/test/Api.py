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
from Inc.Var.Obj import Iif
from IncP.CtrlBase import TCtrlBase
from . import Util


class TMain(TCtrlBase):
    async def Main(self, **aData: dict) -> dict:
        pass

    async def Parse(self, aUrl: str, aScript: str, aEmul: bool) -> dict:
        if (aUrl):
            UrlData = await Util.Cache.Download(aUrl, aEmul)
            if (UrlData['status'] != 200):
                return {'err': f'download status code {UrlData["status"]}'}
        else:
            return {'err': 'no url'}

        Script = Util.LoadScript(aScript)
        if ('err' in Script):
            return Script

        Type = list(Script.keys())[0]
        BSoup = Util.GetSoup(UrlData['data'])
        Scheme = TScheme(Script)
        Scheme.Parse(BSoup)
        Pipe = Scheme.GetPipe(Type)

        Checks = Util.CheckPipe(Pipe, Type)
        PipeStr = json.dumps(Pipe, indent=2, ensure_ascii=False, cls=TJsonEncoder)
        return {
            'err': '\n'.join(Scheme.Err + Checks),
            'data': PipeStr
        }

    async def GetLineNo(self, aScript: str, aErr: str) -> dict:
        Res = {}
        if (re.search(r'\((none|unknown)\)$', aErr)):
            Path = aErr.split('->', maxsplit=1)[0]
            LineNo = FindLineInScheme(aScript, Path)
            Res = {
                'line': LineNo,
                'column': -1
            }
        elif (aErr.startswith('json:')):
            Match = re.search(r'line (\d+) column (\d+)', aErr)
            if (Match):
                Res = {
                    'line': int(Match.group(1)),
                    'column': int(Match.group(2))
                }
        return Res

    async def GetHelp(self) -> dict:
        Help = TSchemeApi.help(None)
        return {'help': Help}

    async def GetTemplate(self, aName: str, aType: str) -> dict:
        match aType:
            case 'new':
                Dbl = await self.ExecModelImport(
                    'scheme',
                    {
                        'method': 'GetSchemeNew',
                        'param': {}
                    }
                )

                Url = Iif(Dbl, Dbl.Rec.url, 'http://your-test-site-here.com')
                Format = {
                    '$date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                    '$url': Url
                }
                DictRepl = TDictRepl(Format)
                CurDir = __package__.replace('.', '/')
                Script = DictRepl.ParseFile(f'{CurDir}/fmt_{aName}.json')
            case 'rnd':
                Dbl = await self.ExecModelImport(
                    'scheme',
                    {
                        'method': 'GetSchemeRnd',
                        'param': {}
                    }
                )
                Pair = Dbl.ExportPair('url_en', 'scheme')
                Script = Pair.get(aName)
            case _:
                Script = ''

        return {
            'script': Script
        }

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
