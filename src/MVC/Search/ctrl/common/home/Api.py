# Created: 2024.04.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibCtrl as Lib

class TMain(Lib.TCtrlBase):
    async def Main(self, **aData):
        aLangId, aCountryId = Lib.GetDictDefs(
            aData.get('query'),
            ('lang_id', 'country_id'),
            (1, 1)
        )

        DblCategory = await Lib.Model_GetCategoriesCountry(self, aCountryId)
        Categories = DblCategory.ExportList('category')
        ImageUrls = await Lib.Img_GetCategory(self, Categories)
        Translate = await self.Translate(aLangId, Categories)
        DblCategory.AddFieldsFill(['lang', 'href', 'image'], False)
        for xImage, Rec in zip(ImageUrls, DblCategory):
            Category = Rec.category
            Lang = Translate.get(Category, Category)
            Href = f'/?route=product/category&lang_id={aLangId}&country_id={aCountryId}&f_category={Category}'
            DblCategory.RecMerge([Lang, Href, xImage])

        DblLast = await self.ExecModelImport(
            'product',
            {
                'method': 'GetProductsLastAdded',
                'param': {
                    'aCountryId': aCountryId,
                    'aLimit': 5
                },
                'cache_age': 60*10
            }
        )
        DblLast.AddFieldsFill(['href', 'href_ext'], False)
        for Rec in DblLast:
            Href = f'/?route=product/product&lang_id={aLangId}&url_id={Rec.url_id}'
            DblLast.RecMerge([Href, None])

        if (self.GetConf('seo_url')):
            await Lib.SeoEncodeDbl(self, DblCategory, ['href'])
            await Lib.SeoEncodeDbl(self, DblLast, ['href'])

        return {
            'dbl_category': DblCategory.Export(),
            'dbl_products': DblLast.Export()
        }
