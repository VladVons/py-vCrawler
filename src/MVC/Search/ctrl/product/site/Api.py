# Created: 2024.12.20
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from base64 import b64encode
from urllib.parse import quote
import IncP.LibCtrl as Lib

class TMain(Lib.TCtrlBase):
    async def _GetAttrCountFilter(self, aCountryId: int, aFilter: dict) -> dict:
        Category = aFilter.get('category')
        DblAttrAll = await self.ExecModelImport(
            'category',
            {
                'method': 'GetAttrCountInCategorySite',
                'param': {
                    'aCountryId': aCountryId,
                    'aCategory': Category
                },
                'cache_age': 60*10
            }
        )

        # not only category attr
        if (len(aFilter) > 1):
            DblAttr = await self.ExecModelImport(
                'category',
                {
                    'method': 'GetAttrCountFilter',
                    'param': {
                        'aCountryId': aCountryId,
                        'aFilter': aFilter
                    }
                }
            )

            Pairs = DblAttr.ExportPairs('key', ['total', 'stat'], True)
            DblAttrAll.ToList()
            for xRec in DblAttrAll:
                Total = 0
                Stat = {xKey: 0 for xKey in xRec.stat}
                Data = Pairs.get(xRec.key)
                if (Data):
                    Total = Data['total']
                    Stat |= Data['stat']
                xRec.total = Total
                xRec.stat = Stat
        return DblAttrAll

    async def Api_GetAttrCountFilter(self, aCountryId: int, aFilter: dict) -> dict:
        for xKey, xVal in aFilter.items():
            if ('size' in xKey) and (xVal):
                aFilter[xKey] = int(xVal)

        Dbl = await self._GetAttrCountFilter(aCountryId, aFilter)
        return Dbl.Export()

    async def Main(self, **aData):
        aLangId, aSiteId, aPage, aLimit = Lib.GetDictDefs(
            aData.get('query'),
            ('lang_id', 'site_id', 'page', 'limit'),
            (1, 1, 1, self.GetConf('products_per_page', 10))
        )

        aOrder = 'price'
        aLimit = min(aLimit, self.GetConf('products_per_page_max', 100))

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

        Filter = Lib.GetFilterFromQuery(aData.get('query'))
        Category = Filter.get('category')

        ImageUrl = await Lib.Img_GetCategory(self, [Category])
        Info = DblInfo.Rec.GetAsDict()
        Res = {
            'info': Info,
            'host': Lib.UrlToDict(Info['url'])['host'],
            'lang_id': aLangId,
            'category': Category,
            'image': ImageUrl[0]
        }

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

        DblAttr = await self._GetAttrCountFilter(aSiteId, Filter)
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
        Res['category'] = Category
        Res['site_id'] = aSiteId
        Res['href'] = {
            'site': f'/?route=site/site&lang_id={aLangId}&site_id={aSiteId}',
            'btn_attr': f'/?route=product/site&lang_id={aLangId}&f_category={Category}'
        }
        return Res
