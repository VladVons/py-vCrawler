# Created: 2024.12.16
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from base64 import b64encode
from urllib.parse import quote
from IncP.CtrlBase import TCtrlBase, Lib


class TMain(TCtrlBase):
    async def Main(self, **aData):
        aCountryId, aCategory, aPage, aLimit = Lib.GetDictDefs(
            aData.get('query'),
            ('country_id', 'category', 'page', 'limit'),
            (1, '', 1, 10)
        )

        aOrder = 'price'
        aLimit = min(aLimit, 10)

        if (not Lib.IsDigits([aPage, aLimit])):
            return {'status_code': 404}

        Filter = {'category': aCategory}
        DblProducts = await self.ExecModelImport(
            'product',
            {
                'method': 'GetProductsSearchAttr',
                'param': {
                    'aCountryId': aCountryId,
                    'aFilter': Filter,
                    'aOrder': f'{aOrder}',
                    'aLimit': aLimit,
                    'aOffset': (aPage - 1) * aLimit
                }
            }
        )

        Res = {}
        if (not DblProducts):
            Res['dbl_products'] = DblProducts.Export()
            return Res

        Marker = 'findwares.com'
        Hash = quote(b64encode(Marker.encode()).decode('utf-8'))
        DblProducts.AddFieldsFill(['href_int', 'href_ext'], False)
        for Rec in DblProducts:
            HrefInt = f'/?route=product/product&url_id={Rec.url_id}'
            HrefExt = Rec.url + Lib.Iif('?' in Rec.url, '&', '?') + f'srsltid={Hash}'
            DblProducts.RecMerge([HrefInt, HrefExt])

        Pagination = Lib.TPagination(aLimit, aData['path_qs'])
        Pagination.Visible = 7
        PData = Pagination.Get(DblProducts.Rec.total, aPage)
        DblPagination = Lib.TDbList(['page', 'title', 'href', 'current'], PData)

        Res['dbl_products'] = DblProducts.Export()
        Res['dbl_pagenation'] = DblPagination.Export()
        return Res
