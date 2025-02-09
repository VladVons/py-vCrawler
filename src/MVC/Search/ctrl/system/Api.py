# Created: 2025.01.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibCtrl as Lib

class TMain(Lib.TCtrlBase):
    async def RegSession(self, aIp: str, aUAgent: str, aLocation: str) -> dict:
        return await self.ExecModel(
            'system',
            {
                'method': 'RegSession',
                'param': {
                    'aIp': aIp,
                    'aUAgent': aUAgent,
                    'aLocation': aLocation
                }
            }
        )

    async def OnExec(self, **aData: dict) -> dict:
        SessionId = Lib.DeepGetByList(aData, ['session', 'keys', 'session_id'])
        if (SessionId):
            await self.ExecModel(
                'system',
                {
                    'method': 'Ins_HistPageView',
                    'param': {
                        'aSessionId': SessionId,
                        'aUrl': aData['path_qs']
                    }
                }
            )
