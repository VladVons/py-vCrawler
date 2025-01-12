# Created: 2024.04.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from base64 import b64encode
from urllib.parse import quote
import IncP.LibCtrl as Lib


class TMain(Lib.TCtrlBase):
    async def Main(self, **aData):
        aLangId, aCountryId, aSearch, aSort, aOrder, aPage, aLimit = Lib.GetDictDefs(
            aData.get('query'),
            ('lang_id', 'country_id', 'q', 'sort', 'order', 'page', 'limit'),
            (1, 1, '', ('sort_order, title', 'title', 'price', 'stock'), ('asc', 'desc'), 1, self.GetConf('products_per_page', 10))
        )

        aLimit = min(aLimit, self.GetConf('products_per_page_max', 100))

        DblProducts = await self.ExecModelImport(
            'product',
            {
                'method': 'Get_Products_Search2',
                'param': {
                    'aFilter': aSearch,
                    'aCountryId': aCountryId,
                    'aOrder': f'{aSort} {aOrder}',
                    'aLimit': aLimit,
                    'aOffset': (aPage - 1) * aLimit
                }
            }
        )

        if (not DblProducts):
            DblProducts = await self.ExecModelImport(
                'product',
                {
                    'method': 'Get_Products_Search1',
                    'param': {
                        'aFilter': aSearch,
                        'aCountryId': aCountryId,
                        'aOrder': f'{aSort} {aOrder}',
                        'aLimit': aLimit,
                        'aOffset': (aPage - 1) * aLimit
                    }
                }
            )

        Res = {}
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
                await Lib.SeoEncodeDbl(self, DblProducts, ['href'])

        Res['dbl_products'] = DblProducts.Export()
        return Res
