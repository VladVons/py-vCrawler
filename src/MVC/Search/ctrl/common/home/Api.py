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

        DblCategories = await Lib.DblGetCategories(self, aLangId, aCountryId, 'country')

        DblLast = await self.ExecModelImport(
            'product',
            {
                'method': 'GetProductsLastCountry',
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

        Res = {
            'dbl_categories': DblCategories,
            'dbl_products': DblLast,
            'meta_descr': Lib.DeepGetByList(aData, ['res', 'lang', 'about_short']),
            'href': {
                'btn_category': f'/?route=product/country&lang_id={aLangId}&country_id={aCountryId}'
            }
        }
        return Res
