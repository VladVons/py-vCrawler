# Created: 2024.04.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.CtrlBase import TCtrlBase

class TMain(TCtrlBase):
    async def Main(self, aData = None):
        return {'t1': 123}
