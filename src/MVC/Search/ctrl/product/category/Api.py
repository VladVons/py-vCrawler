# Created: 2024.12.16
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from base64 import b64encode
from urllib.parse import quote
import IncP.LibCtrl as Lib


class TMain(Lib.TCtrlBase):
    async def Main(self, **aData):
        aLangId, aCountryId, aPage, aLimit = Lib.GetDictDefs(
            aData.get('query'),
            ('lang_id', 'country_id', 'page', 'limit'),
            (1, 1, 1, self.GetConf('products_per_page', 10))
        )

        aOrder = 'price'
        aLimit = min(aLimit, self.GetConf('products_per_page_max', 100))
        Res = {}

        Filter = Lib.GetFilterFromQuery(aData.get('query'))
        if (not Filter):
            return Res

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

        Res = {
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

        if (DblProducts):
            Marker = 'findwares.com'
            Hash = quote(b64encode(Marker.encode()).decode('utf-8'))
            DblProducts.AddFieldsFill(['href', 'href_ext'], False)
            for Rec in DblProducts:
                Href = f'/?route=product/product&lang_id={aLangId}&url_id={Rec.url_id}'
                HrefExt = Rec.url + Lib.Iif('?' in Rec.url, '&', '?') + f'srsltid={Hash}'
                DblProducts.RecMerge([Href, HrefExt])

            Pagination = Lib.TPagination(aLimit, aData['path_qs'])
            Pagination.Visible = self.GetConf('pagination_cnt', 5)
            PData = Pagination.Get(DblProducts.Rec.total, aPage)
            DblPagination = Lib.TDbList(['page', 'title', 'href', 'current'], PData)
            Res['dbl_pagenation'] = DblPagination.Export()

        if (self.GetConf('seo_url')):
            await Lib.SeoEncodeDbl(self, DblProducts, 'href')

        Res['dbl_products'] = DblProducts.Export()
        Res['category'] = Category
        Res['href'] = {
            'btn': f'/?route=product/category&lang_id={aLangId}&country_id={aCountryId}&f_category={Category}'
        }
        return Res
