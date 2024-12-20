# Created: 2024.12.16
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from base64 import b64encode
from urllib.parse import quote
from IncP.CtrlBase import TCtrlBase, Lib

class TMain(TCtrlBase):
    async def Main(self, **aData):
        aLangId, aCountryId, aPage, aLimit = Lib.GetDictDefs(
            aData.get('query'),
            ('lang_id', 'country_id', 'page', 'limit'),
            (1, 1, 1, 10)
        )

        if (not Lib.IsDigits([aLangId, aCountryId, aPage, aLimit])):
            return {'status_code': 404}

        aOrder = 'price'
        aLimit = min(aLimit, 25)

        Filter = Lib.GetFilterFromQuery(aData.get('query'))
        if (not Filter):
            return {}

        Res = {}
        Category = Filter.get('category')
        DblAttr = await self.ExecModelImport(
            'category',
            {
                'method': 'GetAttrCountInCategory',
                'param': {
                    'aCountryId': aCountryId,
                    'aCategory': Category
                },
                'cache_age': 60*10
            }
        )

        Res['info'] = {
            'country_id': aCountryId,
            'lang_id': aLangId,
            'category': Category
        }

        DblAttr.AddFieldsFill(['active'], False)
        for Rec in DblAttr:
            Filtered = Filter.get(Rec.key)
            DblAttr.RecMerge([str(Filtered)])
        Res['dbl_attr'] = DblAttr.Export()

        DblProducts = await self.ExecModelImport(
            'product',
            {
                'method': 'GetProductsAttrCountry',
                'param': {
                    'aCountryId': aCountryId,
                    'aFilter': Filter,
                    'aOrder': f'{aOrder}',
                    'aLimit': aLimit,
                    'aOffset': (aPage - 1) * aLimit
                }
            }
        )

        if (not DblProducts):
            Res['dbl_products'] = DblProducts.Export()
            return Res

        Marker = 'findwares.com'
        Hash = quote(b64encode(Marker.encode()).decode('utf-8'))
        DblProducts.AddFieldsFill(['href_int', 'href_ext'], False)
        for Rec in DblProducts:
            HrefInt = f'/?route=product/product&lang_id={aLangId}&url_id={Rec.url_id}'
            HrefExt = Rec.url + Lib.Iif('?' in Rec.url, '&', '?') + f'srsltid={Hash}'
            DblProducts.RecMerge([HrefInt, HrefExt])

        Pagination = Lib.TPagination(aLimit, aData['path_qs'])
        Pagination.Visible = 7
        PData = Pagination.Get(DblProducts.Rec.total, aPage)
        DblPagination = Lib.TDbList(['page', 'title', 'href', 'current'], PData)

        Res['dbl_products'] = DblProducts.Export()
        Res['dbl_pagenation'] = DblPagination.Export()
        Res['info'] = {
            'country_id': aCountryId,
            'lang_id': aLangId,
            'category': Category
        }
        return Res
