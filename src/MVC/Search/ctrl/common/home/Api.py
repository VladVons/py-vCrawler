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

        DblCategory = await self.ExecModelImport(
            'category',
            {
                'method': 'GetCategoriesCountry',
                'param': {
                    'aCountryId': aCountryId
                },
                'cache_age': 60*10
            }
        )

        Translate = await self.Translate(aLangId, DblCategory.ExportList('category'))
        DblCategory.AddFieldsFill(['lang', 'href'], False)
        for Rec in DblCategory:
            Category = Rec.category
            Lang = Translate.get(Category, Category)
            Href = f'/?route=product/category&lang_id={aLangId}&country_id={aCountryId}&f_category={Category}'
            DblCategory.RecMerge([Lang, Href])

        if (self.GetConf('seo_url')):
            await Lib.SeoEncodeDbl(self, DblCategory, ['href'])

        return {
            'dbl_category': DblCategory.Export()
        }
