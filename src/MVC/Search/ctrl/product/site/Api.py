# Created: 2024.12.20
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from base64 import b64encode
from urllib.parse import quote
from IncP.CtrlBase import TCtrlBase, Lib

class TMain(TCtrlBase):
    async def Main(self, **aData):
        aLangId, aSiteId, aPage, aLimit = Lib.GetDictDefs(
            aData.get('query'),
            ('lang_id', 'site_id', 'page', 'limit'),
            (1, 1, 1, 10)
        )

        aOrder = 'price'
        aLimit = min(aLimit, 20)

        DblInfo = await self.ExecModelImport(
            'site',
            {
                'method': 'GetSiteInfo',
                'param': {
                    'aSiteId': aSiteId,
                    'aLangId': aLangId
                }
           }
        )
        if (not DblInfo):
            return {'status_code': 404}

        Res = {}
        Filter = Lib.GetFilterFromQuery(aData.get('query'))
        Category = Filter.get('category')

        Info = DblInfo.Rec.GetAsDict()
        Info['host'] = Lib.UrlToDict(Info['url'])['host']
        Info['lang_id'] = aLangId
        Info['category'] = Category
        Res['info'] = Info

        if (not Filter):
            return Res

        DblAttr = await self.ExecModelImport(
            'category',
            {
                'method': 'GetAttrCountInCategorySite',
                'param': {
                    'aSiteId': aSiteId,
                    'aCategory': Category
                }
            }
        )

        DblAttr.AddFieldsFill(['active'], False)
        for Rec in DblAttr:
            Filtered = Filter.get(Rec.key)
            DblAttr.RecMerge([str(Filtered)])
        Res['dbl_attr'] = DblAttr.Export()

        DblProducts = await self.ExecModelImport(
            'product',
            {
                'method': 'GetProductsAttrSite',
                'param': {
                    'aSiteId': aSiteId,
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

        return Res
