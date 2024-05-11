# Created: 2024.04.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Loader.Lang import TLoaderLangFs
from Inc.Misc.Time import SecondsToDHMS_Str
from Inc.Misc.Jinja import TFileSystemLoader, TEnvironment
from Inc.Sql import TDbExecPool, TDbMeta, TDbPg
from Inc.Sql.ADb import TDbAuth
from IncP.ApiBase import TApiBase
from IncP.Plugins import TModels
from IncP.Log import Log, TEchoDb
import IncP.LibModel as Lib


class TApiModel(TApiBase):
    def __init__(self):
        super().__init__()

        Conf = self.GetConf()
        DbAuth = Conf['db_auth']
        self.DbAuth = TDbAuth(**DbAuth)
        Db = TDbPg(self.DbAuth)
        self.DbMeta = TDbMeta(Db)

        Loader = TFileSystemLoader()
        self.Env = TEnvironment(loader = Loader)

        self.Plugin = TModels(Conf['dir_route'], self)
        self.Helper = {'route': 'system', 'method': 'Api'}

        Section = Conf['loader']['lang']
        if (Section['type'] == 'fs'):
            Def = Lib.GetDictDef(Section, ['dir'], ['MVC/lang'])
            self.Lang = TLoaderLangFs(*Def)
        else:
            raise ValueError()

    async def DbConnect(self):
        await self.DbMeta.Db.Connect()
        await self.DbMeta.Init()

        Dbl = await self.DbMeta.Db.GetDbVersion()
        Version = Dbl.Rec.version.split()[:2]
        Log.Print(1, 'i',
            'Server: %s, Uptime: %s, DbName: %s, DbSize: %sM, Tables %s' %
            (
                ' '.join(Version),
                SecondsToDHMS_Str(Dbl.Rec.uptime.seconds),
                Dbl.Rec.db_name,
                round(Dbl.Rec.size / 1000000, 2),
                Dbl.Rec.tables
            )
        )

        if (Dbl.Rec.tables == 0):
            Log.Print(1, 'i', 'Database is empty. Creating tables ...')
            await TDbExecPool(self.DbMeta.Db.Pool).ExecFile(f'{self.Plugin.Dir}/dbTable.sql')
            await TDbExecPool(self.DbMeta.Db.Pool).ExecFile(f'{self.Plugin.Dir}/dbMeta.sql')
            await TDbExecPool(self.DbMeta.Db.Pool).ExecFile(f'{self.Plugin.Dir}/dbApp.sql')
            #await TDbExecPool(self.DbMeta.Db.Pool).ExecFile(f'{self.Models.Dir}/dbData.sql')

        Log.AddEcho(TEchoDb(self.DbMeta.Db))

    async def DbClose(self):
        List = Log.FindEcho(TEchoDb.__name__)
        if (List):
            Log.Echoes.remove(List[0])

        if (self.DbMeta):
            await self.DbMeta.Db.Close()


ApiModel = TApiModel()
