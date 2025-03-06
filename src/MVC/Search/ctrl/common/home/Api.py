# Created: 2024.04.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibCtrl as Lib

class TMain(Lib.TCtrlBase):
    async def OnFinal(self, **aData):
        return {
            'meta_descr': Lib.DeepGetByList(aData, ['res', 'lang', 'about_short'])
        }

    async def Main(self, **aData):
        aLangId, aCountryId = Lib.GetDictDefs(
            aData.get('query'),
            ('lang_id', 'country_id'),
            (1, 1)
        )

        DblCategories = await Lib.DblGetCategories(self, aLangId, aCountryId, 'country')

        DblLast = await self.ExecModelImport(
            'product',
            {
                'method': 'GetProductsLastAdded',
                'param': {
                    'aCountryId': aCountryId,
                    'aLimit': 5
                },
                'cache_age': -1
            }
        )
        Lib.DblProducts_Adjust(DblLast, aLangId)


        if (self.GetConf('seo_url')):
            await Lib.SeoEncodeDbl(self, DblCategories, ['href'])
            await Lib.SeoEncodeDbl(self, DblLast, ['href'])

        return {
            'dbl_categories': DblCategories,
            'dbl_products': DblLast,
            'exec': {'method': 'OnFinal'}
        }
