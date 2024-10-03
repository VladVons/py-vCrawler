# Created: 2024.10.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.DbList import TDbList
from Inc.ParserX.Common import TFileBase
from Inc.Sql import TDbExecPool, TDbPg


class TMain(TFileBase):
    def __init__(self, aParent, aDb: TDbPg):
        super().__init__(aParent)
        self.Db = aDb

    async def Upload(self):
        Dbl = TDbList().Import(self.Parent.Conf['sites'])
        for Rec in Dbl:
            if (Rec.enable):
                for xType in Rec.type:
                    if (not xType.startswith('-')):
                        Query = f'''
                            delete from {xTable}
                        '''
                        await TDbExecPool(self.Db.Pool).Exec(Query)
