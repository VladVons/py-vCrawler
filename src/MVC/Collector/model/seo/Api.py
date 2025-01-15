# Created: 2025.01.205
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibModel as Lib

class TMain(Lib.TDbModel):
    async def Get_SeoToDict(self, aPath: list[str]) -> dict:
        Arr = [f"(keyword = '{x}' or keyword like '%/{x}')" for x in aPath]
        CondKeyword = ' or\n'.join(Arr)
        return await self.ExecQuery(
            'fmtGet_SeoToDict.sql',
            {
                'CondKeyword': CondKeyword
            }
        )

    async def Get_SeoFromDict(self, aData: list) -> dict:
        Data = [f"({Idx}, '{Key}', '{Lib.Escape(Val)}')" for Idx, Key, Val in aData]
        return await self.ExecQuery(
            'fmtGet_SeoFromDict.sql',
            {
                'Data': ', '.join(Data)
            }
        )

    async def Get_SeoRedirect(self, aPath: str) -> dict:
        return await self.ExecQuery(
            'fmtGet_SeoRedirect.sql',
            {
                'aPath': aPath
            }
        )
