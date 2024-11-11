# Created: 2024.10.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import json
#
from Inc.DbList import TDbList
from Inc.Http.HttpUrl import UrlToDict, UrlToStr
from Inc.Misc.Template import FormatFilePkg
from Inc.ParserX.Common import TFileBase
from Inc.ParserX.CommonSql import DASplitDbl
from Inc.Sql import TDbExecPool, TDbPg
from Inc.Var.Dict import DeepGetByList
from Inc.Var.Str import JsonFormat, JsonKeyPos
from IncP.Log import Log
from .. import SiteCondEnabled


def FormatJson(aJson: str, aUrl: str) -> str:
    Pos = JsonKeyPos(aJson, 'info')
    if (Pos):
        Lines = [
            Line
            for Idx, Line in enumerate(aJson.splitlines())
            if (not Pos[0] <= Idx <= Pos[1])
        ]
        Repl = f'"url": "{aUrl}"'
        Lines.insert(Pos[0], Repl)
        aJson = '\n'.join(Lines)

    Res = JsonFormat(aJson)
    json.loads(Res) # just check json
    return Res


class TMain(TFileBase):
    def __init__(self, aParent, aDb: TDbPg):
        super().__init__(aParent)
        self.Db = aDb

    async def Upload(self):
        @DASplitDbl
        async def SSite(aDbl: TDbList, _aMax: int, _aIdx: int = 0, _aLen: int = 0):
            async def FilterExisted(aDbl: TDbList) -> TDbList:
                Hosts = [UrlToStr(UrlToDict(Rec.url), 'host') for Rec in aDbl]
                Hosts = [f"'%{xHost}%'" for xHost in Hosts]
                Query = FormatFilePkg(__package__, 'fmtGet_HostsInUrl.sql', {
                    'aHosts': ', '.join(Hosts)
                })
                DblHosts = await TDbExecPool(self.Db.Pool).Exec(Query)
                Hosts = DblHosts.ExportList('host')

                DblRes = aDbl.New()
                for Rec in aDbl:
                    Host = UrlToDict(Rec.url)['host']
                    if (Host in Hosts):
                        Log.Print(1, 'i', f'Host {Host} already in DB')
                    else:
                        DblRes.RecAdd(Rec.Data)
                return DblRes

            #--- Site
            #Dbl = await FilterExisted(aDbl)
            #if (Dbl.GetSize() == 0):
            #    return
            Dbl = aDbl

            InsValues = []
            SelValues = []
            for Rec in Dbl:
                InsValues.append(f"('{Rec.url}', 1)")
                SelValues.append(f"'{Rec.url}'")

            Query = FormatFilePkg(__package__, 'fmtSet_Site.sql', {
                'InsValues': ', '.join(InsValues),
                'SelValues': ', '.join(SelValues)
            })
            DblRes = await TDbExecPool(self.Db.Pool).Exec(Query)
            Pairs = DblRes.ExportPair('url', 'id')

            #--- SiteParser
            InsValues = []
            DirData = self.Parent.Conf['dir_data']
            for Rec in Dbl:
                for xType in Rec.type:
                    if (not xType.startswith('-')):
                        Path = f'{DirData}/{Rec.dir}/{xType}.json'
                        assert(os.path.exists(Path)), f'Path does not exist {Path}'
                        with open(Path, 'r', encoding='utf8') as F:
                            Scheme = F.read()

                        Scheme = FormatJson(Scheme, Rec.url)
                        SiteId = Pairs[Rec.url]
                        InsValues.append(f"(true, {SiteId}, '{xType}', '{Scheme}')")

            if (InsValues):
                Log.Print(1, 'i', f'Updated parser {len(InsValues)}')
                Query = FormatFilePkg(__package__, 'fmtSet_SiteParser.sql', {'InsValues': ', '.join(InsValues)})
                await TDbExecPool(self.Db.Pool).Exec(Query)

            #--- SiteCategory
            InsValues = []
            for Rec in Dbl:
                if (Rec.category):
                    SiteId = Pairs[Rec.url]
                    for xCategory in Rec.category:
                        InsValues.append(f"(true, {SiteId}, '{xCategory}')")

            if (InsValues):
                Log.Print(1, 'i', f'Updated category {len(InsValues)}')
                Query = FormatFilePkg(__package__, 'fmtSet_SiteCategory.sql', {'InsValues': ', '.join(InsValues)})
                await TDbExecPool(self.Db.Pool).Exec(Query)

        Dbl = TDbList().Import(self.Parent.Conf['sites'])
        Dbl = SiteCondEnabled(Dbl)

        ConfParts = DeepGetByList(self.Parent.Conf, ['sql', 'parts'], 10)
        await SSite(Dbl, ConfParts)
