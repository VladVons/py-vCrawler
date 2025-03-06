# Created: 2024.12.20
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

import IncP.LibCtrl as Lib

class TMain(Lib.TCtrlBase):
    async def _GetAttrCount(self, aSiteId: int, aCategory: str) -> Lib.TDbList:
        return await self.ExecModelImport(
            'category',
            {
                'method': 'GetAttrCountCategorySite',
                'param': {
                    'aSiteId': aSiteId,
                    'aCategory': aCategory
                },
                'cache_age': -1
            }
        )

    async def _GetAttrCountFilter(self, aSiteId: int, aFilter: dict) -> dict:
        Category = aFilter.get('category')
        DblAttrAll = await self._GetAttrCount(aSiteId, Category)

        # not only category attr
        if (len(aFilter) > 1):
            DblAttr = await self.ExecModelImport(
                'category',
                {
                    'method': 'GetAttrCountFilterSite',
                    'param': {
                        'aSiteId': aSiteId,
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

    async def Api_GetAttrCountFilter(self, aSiteId: int, aFilter: dict) -> dict:
        for xKey, xVal in aFilter.items():
            if ('size' in xKey) and (xVal):
                aFilter[xKey] = int(xVal)

        Dbl = await self._GetAttrCountFilter(aSiteId, aFilter)
        return Dbl.Export()


    async def Main(self, **aData) -> dict:
        aLangId, aSiteId, aPage, aLimit, aSort, aOrder = Lib.GetDictDefs(
            aData.get('query'),
            ('lang_id', 'site_id', 'page', 'limit', 'sort', 'order'),
            (1, 1, 1, self.GetConf('products_per_page', 10), ('update_date', 'create_date', 'price'), '')
        )

        if (not aOrder):
            aOrder = Lib.GetSortOrder(aSort)

        aLimit = min(aLimit, self.GetConf('products_per_page_max', 100))

        Res = {}
        Filter = Lib.GetFilterFromQuery(aData.get('query'))
        if (not Filter):
            return Res

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
            'category': Category,
            'image': ImageUrl[0]
        }

        Category = Filter.get('category')
        ImageUrl = await Lib.Img_GetCategory(self, [Category])
        Res = {
            'category': Category,
            'image': ImageUrl[0],
            'dbl_breadcrumbs': Lib.DblGetBreadcrumbs([[Category, '']])
        }

        Dbl = await Lib.Model_GetCategoriesSite(self, aSiteId)
        Rec = Dbl.FindFieldGo('category', Category)
        if (Rec):
            Res['category_cnt'] = Rec.count
            Res['price_min'] = Rec.price_min
            Res['price_max'] = Rec.price_max

        Dbl = await self._GetAttrCount(aSiteId, Category)
        Res['attr_cnt'] = Dbl.ExportPair('key', 'total')

        DblAttr = await self._GetAttrCountFilter(aSiteId, Filter)
        DblAttr.AddFieldsFill(['active'], False)
        for Rec in DblAttr:
            Filtered = Filter.get(Rec.key)
            DblAttr.RecMerge([str(Filtered)])
        Res['dbl_attr'] = DblAttr

        DblProducts = await self.ExecModelImport(
            'product',
            {
                'method': 'GetProductsAttrSite',
                'param': {
                    'aSiteId': aSiteId,
                    'aFilter': Filter,
                    'aOrder': f'{aSort} {aOrder}',
                    'aLimit': aLimit,
                    'aOffset': (aPage - 1) * aLimit
                }
            }
        )

        if (DblProducts):
            Lib.DblProducts_Adjust(DblProducts, aLangId)

            Pagination = Lib.TPagination(aLimit, aData['path_qs'])
            Pagination.Visible = self.GetConf('pagination_cnt', 5)
            PData = Pagination.Get(DblProducts.Rec.total, aPage)
            DblPagination = Lib.TDbList(['page', 'title', 'href', 'current'], PData)
            Res['dbl_pagenation'] = DblPagination

            DblProductsSort = Lib.GetProductsSort(Pagination.Href, f'&sort={aSort}&order={aOrder}')
            Res['dbl_products_sort'] = DblProductsSort

        DblCategories = await Lib.DblGetCategories(self, aLangId, aSiteId, 'site')

        if (self.GetConf('seo_url')):
            await Lib.SeoEncodeDbl(self, DblProducts, ['href', 'href_int'])
            await Lib.SeoEncodeDbl(self, DblCategories, ['href'])

        Res['type'] = 'site'
        Res['dbl_products'] = DblProducts
        Res['dbl_categories'] = DblCategories
        Res['category'] = Category
        Res['href'] = {
            'btn_attr': f'/?route=product/site&lang_id={aLangId}&site_id={aSiteId}&f_category={Category}'
        }
        return Res
