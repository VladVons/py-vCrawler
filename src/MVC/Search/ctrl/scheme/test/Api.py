# Created: 2024.04.21
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
import json
#
from Inc.DbList.DbUtil import TJsonEncoder
from Inc.Scheme.Scheme import TScheme, TSchemeApi
from Inc.Scheme.Utils import FindLineInScheme
from Inc.Util.ModHelp import GetClass
from IncP.CtrlBase import TCtrlBase, Lib
from .Util import GetSoup, UrlGetData


class TMain(TCtrlBase):
    async def Main(self, **aData: dict) -> dict:
        pass

    async def Parse(self, aScript: str) -> dict:
        try:
            Script = json.loads(aScript)
            Type = list(Script.keys())[0]
        except Exception as E:
            return {'err': f'json: {E}'}

        Urls = Lib.DeepGetByList(Script, [Type, 'info', 'url'])
        if (Urls):
            if (not isinstance(Urls, list)):
                return {'err': f'not a list: {Type}->info->url'}
            Urls = [xUrl for xUrl in Urls if xUrl.startswith('http')]
            if (not Urls):
                return {'err': 'no urls with http prefix'}

            UrlData = await UrlGetData(Urls[0])
            if (UrlData['status'] != 200):
                return {'err': f'download status code {UrlData["status"]}'}
        else:
            UrlData = {
                'data': f'''
                    <html>
                        <body>
                            No {Type}->info->url section found !
                            The quick brown fox jumps over the lazy dog.
                        </body>
                    </html>
                '''
            }

        BSoup = GetSoup(UrlData['data'])
        Scheme = TScheme(Script)
        Scheme.Parse(BSoup)
        Pipe = Scheme.GetPipe(Type)

        PipeStr = json.dumps(Pipe, indent=2, ensure_ascii=False, cls=TJsonEncoder)
        return {
            'err': '\n'.join(Scheme.Err),
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

    async def GetHelp(self, aScript: str) -> dict:
        Help = TSchemeApi.help(None)
        return {'help': Help}
