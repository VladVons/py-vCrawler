# Created: 2023.09.26
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.ParserX.Common import TFileBase
from Inc.Sql import TDbExecPool, TDbPg
from IncP.Log import Log


class TMain(TFileBase):
    def __init__(self, aParent, aDb: TDbPg):
        super().__init__(aParent)
        self.Db = aDb

    async def Clear(self):
        Dbl = await self.Db.GetPrimaryKeys(aType = 'PRIMARY KEY')
        TablesPrimary = Dbl.ExportPair('table_name', 'column_name')

        Tables = self.Parent.Conf.GetKey('tables')
        for xTable in Tables:
            if (not xTable.startswith('-')):
                Log.Print(1, 'i', f'Clear(), {xTable}')

                Query = f'''
                    delete from {xTable}
                '''
                await TDbExecPool(self.Db.Pool).Exec(Query)

                Column = TablesPrimary.get(xTable)
                if (Column == 'id'):
                    Query = f'''
                        alter sequence {xTable}_id_seq restart 1
                    '''
                    await TDbExecPool(self.Db.Pool).Exec(Query)

                    Query = f'''
                        alter table {xTable} alter id set default nextval('{xTable}_id_seq')
                    '''
                    await TDbExecPool(self.Db.Pool).Exec(Query)
