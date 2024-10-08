# Created: 2024.10.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import json
#
from Inc.DbList import TDbList
from Inc.ParserX.Common import TFileBase
from Inc.ParserX.CommonSql import LoadQuery, DASplitDbl
from Inc.Var.Dict import DeepGetByList
from Inc.Sql import TDbExecPool, TDbPg
from IncP.Log import Log
from .. import SiteCondEnabled


class TMain(TFileBase):
    def __init__(self, aParent, aDb: TDbPg):
        super().__init__(aParent)
        self.Db = aDb

    async def Upload(self):
        @DASplitDbl
        async def SSite(aDbl: TDbList, _aMax: int, _aIdx: int = 0, _aLen: int = 0):

            #--- Site
            InsValues = []
            SelValues = []
            for Rec in aDbl:
                InsValues.append(f"('{Rec.url}', 1)")
                SelValues.append(f"'{Rec.url}'")

            Query = LoadQuery(__package__, 'fmtSet_Site.sql', {
                'InsValues': ', '.join(InsValues),
                'SelValues': ', '.join(SelValues)
            })
            DblRes = await TDbExecPool(self.Db.Pool).Exec(Query)
            Pairs = DblRes.ExportPair('url', 'id')

            #--- SiteParser
            InsValues = []
            DirData = self.Parent.Conf['dir_data']
            for Rec in aDbl:
                for xType in Rec.type:
                    if (not xType.startswith('-')):
                        Path = f'{DirData}/{Rec.dir}/{xType}.json'
                        assert(os.path.exists(Path)), f'Path does not exist {Path}'
                        with open(Path, 'r', encoding='utf8') as F:
                            Scheme = F.read()
                            json.loads(Scheme) # just check

                        SiteId = Pairs[Rec.url]
                        InsValues.append(f"(true, {SiteId}, '{xType}', '{Scheme}')")

            if (InsValues):
                Log.Print(1, 'i', f'Updated parser {len(InsValues)}')
                Query = LoadQuery(__package__, 'fmtSet_SiteParser.sql', {'InsValues': ', '.join(InsValues)})
                await TDbExecPool(self.Db.Pool).Exec(Query)

            #--- SiteCategory
            InsValues = []
            for Rec in aDbl:
                if (Rec.category):
                    SiteId = Pairs[Rec.url]
                    for xCategory in Rec.category:
                        InsValues.append(f"(true, {SiteId}, '{xCategory}')")

            if (InsValues):
                Log.Print(1, 'i', f'Updated category {len(InsValues)}')
                Query = LoadQuery(__package__, 'fmtSet_SiteCategory.sql', {'InsValues': ', '.join(InsValues)})
                await TDbExecPool(self.Db.Pool).Exec(Query)

        Dbl = TDbList().Import(self.Parent.Conf['sites'])
        Dbl = SiteCondEnabled(Dbl)

        ConfParts = DeepGetByList(self.Parent.Conf, ['sql', 'parts'], 10)
        await SSite(Dbl, ConfParts)
