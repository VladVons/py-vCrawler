# Created: 2024.12.06
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from base64 import b64encode
from Inc.DbList import TDbList
from Inc.DbList.DbConvert import DblToXlsx
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

    async def AsExcel(self, aScript: str) -> dict:
        SpecComp = TSpecComp()
        Fields = list(SpecComp.Parsers.keys())
        Pos = Fields.index('brand')
        Fields.insert(Pos + 1, 'model')
        Fields += ['scr_size', 'scr_res']
        Dbl = TDbList(Fields)

        #RecDef = [''] * len(Fields)
        Lines = SpecComp.GetLines(aScript)
        for xLine in Lines:
            Rec = Dbl.RecAdd()
            #Data = {}
            Spec = SpecComp.Parse(xLine)
            for xKey, xVal in Spec.items():
                if (isinstance(xVal, dict)):
                    Arr = list(map(str, xVal.values()))
                    xVal = ' '.join(Arr)
                elif (isinstance(xVal, list)):
                    xVal = ' '.join(xVal)
                #Data[xKey] = xVal
                Rec.SetField(xKey, xVal)
            #Rec.SetAsDict(Data)

        Xlsx = DblToXlsx([Dbl])
        Data = b64encode(Xlsx).decode('utf-8')
        return {
            'err': '',
            'data': Data
        }

    async def LoadRandom(self) -> dict:
        Dbl = await self.ExecModelImport(
            'scheme',
            {
                'method': 'GetProductsRnd',
                'param': {
                    'aLimit': 100
                }
            }
        )
        Products = Dbl.ExportList('title')

        return {
            'err': '',
            'data': '\n'.join(Products)
        }
