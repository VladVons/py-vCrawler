# Created: 2024.04.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.CtrlBase import TCtrlBase, Lib

class TMain(TCtrlBase):
    async def Main(self, **aData):
        aCountryId, aLangId = Lib.GetDictDefs(
            aData.get('query'),
            ('country_id', 'lang_id'),
            (1, 1)
        )

        DblCategory = await self.ExecModelImport(
            'category',
            {
                'method': 'GetCountryCategories',
                'param': {
                    'aCountryId': aCountryId
                },
                'cache_age': 60*10
            }
        )

        Trans = await self.Translate(aLangId, DblCategory.ExportList('category'))
        DblCategory.AddFieldsFill(['lang', 'href'], False)
        for Rec in DblCategory:
            Category = Rec.category
            Lang = Trans.get(Category, Category)
            Href = f'/?route=product/category&country_id={aCountryId}&lang_id={aLangId}&f_category={Category}'
            DblCategory.RecMerge([Lang, Href])

        return {
            'dbl_category': DblCategory.Export()
        }
