# Created: 2024.04.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibModel as Lib


class TMain(Lib.TDbModel):
    async def GetLayoutLang(self, aLangId: int, aRoute: str) -> dict:
        return await self.ExecQuery(
            'fmtGet_LayoutLang.sql',
            {
              'aLangId': aLangId,
              'aRoute': aRoute
            }
        )

    async def GetAliasLangByList(self, aLangId: int, aText: list[str]) -> dict:
        if (aText):
            Arr = [f"('{xText}')" for xText in aText]
            return await self.ExecQuery(
                'fmtGet_AliasLangByList.sql',
                {
                'aLangId': aLangId,
                'aValues': ', '.join(Arr)
                }
            )

    async def GetAliasLang(self, aLangId: int) -> dict:
        return await self.ExecQuery(
            'fmtGet_AliasLang.sql',
            {
              'aLangId': aLangId
            }
        )

    async def GetLang(self, aLangId: int) -> dict:
        return await self.ExecQuery(
            'fmtGet_Lang.sql',
            {
              'aLangId': aLangId
            }
        )

    async def GetConf(self, aAttr: list[str] = None) -> dict:
        if (aAttr):
            WhereExt = f'attr in ({Lib.ListToComma(aAttr)})'
        else:
            WhereExt = True

        Res = await self.ExecQuery(
            'fmtGet_Conf.sql',
            {
              'WhereExt': WhereExt
            }
        )
        return Res

    async def RegSession(self, aIp: str, aUAgent: str, aLocation: str) -> dict:
        Query = f'''
            insert into hist_session
                (ip, uagent, location)
            values
                ('{aIp}', '{aUAgent[:256]}', '{aLocation}')
            returning (id)
        '''
        return await self.ExecQueryText(Query)

    async def Ins_HistPageView(self, aSessionId: int, aUrl: str) -> dict:
        Query = f'''
            insert into hist_page_view (session_id, url)
            values ({aSessionId}, '{aUrl[:128]}')
        '''
        return await self.ExecQueryText(Query)
