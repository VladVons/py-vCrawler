# Created: 2024.11.11
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibCtrl as Lib

class TMain(Lib.TCtrlBase):
    async def Main(self, **aData) -> dict:
        aLangId, aCountryId, aSearch = Lib.GetDictDefs(
            aData.get('query'),
            ('lang_id', 'country_id', 'q'),
            (1, 1, '')
        )

        DblCountry = await self.ExecModelImport(
            'site',
            {
                'method': 'GetCountries',
                'param': {
                    'aLangId': aLangId
                }
            }
        )
        RecNo = DblCountry.FindField('id', aCountryId)
        Country = '' if (RecNo == -1) else DblCountry.RecGo(RecNo).title

        return  {
            'href': {
               'compare': '/?route=product/compare',
                'counties': f'/?route=site/countries&lang_id={aLangId}',
                'root': f'/?lang_id={aLangId}'
            },
            'search': aSearch,
            'lang_id': aLangId,
            'country_id': aCountryId,
            'country': Country,
            'dbl_country': DblCountry.Export()
        }
