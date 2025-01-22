# Created: 2024.12.06
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from base64 import b64encode
from Inc.Var.Dict import DictToPath
from Inc.DbList.DbConvert import DblToXlsx
from Inc.ParserSpec.LibsComp import TLibsComp
import IncP.LibCtrl as Lib


class TMain(Lib.TCtrlBase):
    async def Main(self, **aData: dict) -> dict:
        pass

    async def ScriptTest(self, aScript: str) -> dict:
        LibsComp = TLibsComp()
        Lines = LibsComp.GetLines(aScript)
        Arr = LibsComp.ParseLines(Lines)

        return {
            'err': '',
            'data': '\n'.join(Arr)
        }

    async def AsExcel(self, aScript: str) -> dict:
        SpecComp = TLibsComp()
        Fields = ['product']
        for xParser in SpecComp.Parsers.values():
            Fields += xParser.GetFields()
        Dbl = Lib.TDbList(Fields)

        Lines = SpecComp.GetLines(aScript)
        for xLine in Lines:
            Rec = Dbl.RecAdd()
            Rec.SetField('product', xLine)
            Spec = SpecComp.Parse(xLine)
            for xKey, xVal in Spec.items():
                if (isinstance(xVal, dict)):
                    Arr = list(map(str, xVal.values()))
                    xVal = ' '.join(Arr)
                elif (isinstance(xVal, list)):
                    xVal = ' '.join(xVal)
                Rec.SetField(xKey, xVal)

        #DblToXlsxSave([Dbl], 'test.xlsx')
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

    async def ProductsNoAttrRefresh(self) -> dict:
        async def _ProductsNoAttrRefresh(aLimit: int) -> int:
            Dbl = await self.ExecModelImport(
                'scheme',
                {
                    'method': 'GetProductsNoAttr',
                    'param': {
                        'aLimit': aLimit
                    }
                }
            )

            Res = len(Dbl)
            if (Res):
                SpecComp = TLibsComp()
                Values = []
                for Rec in Dbl:
                    Attrs = SpecComp.Parse(Rec.title)
                    AttrPath = DictToPath(Attrs)
                    for xKey in list(AttrPath.keys()):
                        xVal = AttrPath[xKey]
                        if (isinstance(xVal, str)):
                            AttrPath[xKey] = xVal.lower()

                        if (xKey in ['cpu/gen', 'ram/unit', 'storage/unit']):
                            del AttrPath[xKey]

                    Values.append((Rec.url_id, Rec.title, AttrPath))

                Dbl = await self.ExecModelImport(
                    'scheme',
                    {
                        'method': 'UpdProductsAttr',
                        'param': {
                            'aValues': Values
                        }
                    }
                )
            return Res

        Cnt = 0
        for i in range(10):
            R = await _ProductsNoAttrRefresh(1000)
            if (R == 0):
                break

            Cnt += R
            print(i+1, 'updated attr ', Cnt)

        return {
            'err': f'updated products {Cnt}',
            'data': ''
        }
