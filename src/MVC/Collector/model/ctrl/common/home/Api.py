# Created: 2024.04.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.ModelBase import TModelBase, Lib

class TMain(TModelBase):
    async def Main(self, aData):
        return {'t1': 123}
