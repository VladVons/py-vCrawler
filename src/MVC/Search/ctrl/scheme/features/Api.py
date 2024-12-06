# Created: 2024.12.06
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from Inc.ParserSpec.TestAll import TSpecComp
from IncP.CtrlBase import TCtrlBase


class TMain(TCtrlBase):
    async def Main(self, **aData: dict) -> dict:
        pass

    async def ScriptTest(self, aScript: str) -> dict:
        SpecComp = TSpecComp()
        Lines = SpecComp.GetLines(aScript)
        Arr = SpecComp.ParseLines(Lines)

        return {
            'err': '',
            'data': '\n'.join(Arr)
        }
