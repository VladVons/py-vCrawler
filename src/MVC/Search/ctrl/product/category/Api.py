# Created: 2024.12.16
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

import IncP.LibCtrl as Lib


class TMain(Lib.TCtrlBase):
    async def _GetAttrCountFilter(self, aCountryId: int, aFilter: dict) -> dict:
        Category = aFilter.get('category')
        DblAttrAll = await self.ExecModelImport(
            'category',
            {
                'method': 'GetAttrCountInCategory',
                'param': {
                    'aCountryId': aCountryId,
                    'aCategory': Category
                },
                'cache_age': -1
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

    async def Main(self, **aData) -> dict:
        aLangId, aCountryId, aPage, aLimit, aSort, aOrder = Lib.GetDictDefs(
            aData.get('query'),
            ('lang_id', 'country_id', 'page', 'limit', 'sort', 'order'),
            (1, 1, 1, self.GetConf('products_per_page', 10), ('update_date', 'create_date', 'price'), '')
        )

        if (not aOrder):
            aOrder = Lib.GetSortOrder(aSort)

        aLimit = min(aLimit, self.GetConf('products_per_page_max', 100))

        Res = {}
        Filter = Lib.GetFilterFromQuery(aData.get('query'))
        if (not Filter):
            return Res

        Category = Filter.get('category')
        DblCategories = await Lib.Model_GetCategoriesCountry(self, aCountryId)
        Rec = DblCategories.FindFieldGo('category', Category)
        CategoryItemsCnt = Lib.Iif(Rec, Rec.count, 0)

        ImageUrl = await Lib.Img_GetCategory(self, [Category])
        Res = {
            'country_id': aCountryId,
            'lang_id': aLangId,
            'category': Category,
            'category_cnt': CategoryItemsCnt,
            'image': ImageUrl[0]
        }

        DblAttr = await self._GetAttrCountFilter(aCountryId, Filter)
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
            Res['dbl_pagenation'] = DblPagination.Export()

            DblProductsSort = Lib.GetProductsSort(Pagination.Href, f'&sort={aSort}&order={aOrder}')
            Res['dbl_products_sort'] = DblProductsSort.Export()

        if (self.GetConf('seo_url')):
            await Lib.SeoEncodeDbl(self, DblProducts, ['href'])

        Res['dbl_products'] = DblProducts.Export()
        Res['category'] = Category
        Res['href'] = {
            'btn_attr': f'/?route=product/category&lang_id={aLangId}&country_id={aCountryId}&f_category={Category}'
        }
        return Res
