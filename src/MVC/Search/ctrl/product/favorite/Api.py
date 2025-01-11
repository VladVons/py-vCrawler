# Created: 2025.01.10
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibCtrl as Lib
from ..._inc.products_a import Main as products_a


class TMain(Lib.TCtrlBase):
    async def Main(self, **aData: dict) -> dict:
        aLangId, aUrlIds, = Lib.GetDictDefs(
            aData.get('query'),
            ('lang_id', 'url_ids'),
            (1, '1,2,3')
        )

        UrlIds = aUrlIds.split(',')
        if (not Lib.IsDigits(UrlIds)):
            return {'status_code': 404}

        Dbl = await self.ExecModelImport(
            'product',
            {
                'method': 'GetProductByUrlIds',
                'param': {
                    'aUrlIds': UrlIds
                }
            }
        )
        if (not Dbl):
            return {'status_code': 404}

        DblProducts = await products_a(self, Dbl)
        return {
            'dbl_products_a': DblProducts.Export()
        }
