# Created: 2024.04.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.CtrlBase import TCtrlBase, Lib


class TMain(TCtrlBase):
    async def Get_UserConf(self, aData: dict) -> dict:
        aUserId = Lib.DeepGetByList(aData, ['param', 'user_id'], 0)
        Dbl = await self.ExecModelImport(
            'user',
            {
                'method': 'Get_UserConf',
                'param': {
                   'aUserId': aUserId
                }
            }
        )
        return Dbl.Export()

    async def Get_UserId(self, aData: dict) -> dict:
        aLogin, aPassw = Lib.GetDictDefs(
            aData.get('param'),
            ('login', 'passw'),
            ('', '')
        )

        Dbl = await self.ExecModelImport(
            'user',
            {
                'method': 'Get_UserId',
                'param': {
                   'aLogin': aLogin,
                   'aPassw': aPassw
                }
            }
        )
        return Dbl.Export()
