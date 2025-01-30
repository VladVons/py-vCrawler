# Created: 2024.11.11
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from datetime import datetime
#
import IncP.LibCtrl as Lib

class TMain(Lib.TCtrlBase):
    async def Main(self, **aData) -> dict:
        aLangId, aCountryId, aSearch = Lib.GetDictDefs(
            aData.get('query'),
            ('lang_id', 'country_id', 'q'),
            (-1, -1, '')
        )

        if (aCountryId == -1) and (aLangId == -1):
            Country = Lib.DeepGetByList(aData, ['session', 'location', 'country'])
            #Country = 'poland'
            if (Country):
                Data = await self.ApiModel(
                    'site',
                    {
                        'method': 'GetCountryLangByName',
                        'param': {
                            'aCountry': Country.strip()
                        }
                    }
                )
                Dbl = Lib.TDbList().Import(Data)
                if (Dbl):
                    aLangId = Dbl.Rec.lang_id
                    aCountryId = Dbl.Rec.country_id

        # ToDo
        aCountryId = Lib.Iif(aCountryId == -1, 1, aCountryId)
        aLangId = Lib.Iif(aLangId == -1, 1, aLangId)

        aData['query']['country_id'] = aCountryId
        aData['query']['lang_id'] = aLangId

        DblCountry = await self.ExecModelImport(
            'site',
            {
                'method': 'GetCountries',
                'param': {
                    'aLangId': aLangId
                },
                'cache_age': -1
            }
        )

        RecNo = DblCountry.FindField('id', aCountryId)
        Country = '' if (RecNo == -1) else DblCountry.RecGo(RecNo).title

        Res = {
            'href_search_ajax': '/api/?route=product/search',
            'href': {
                'countries': f'/?route=site/countries&lang_id={aLangId}',
                'compare':  f'/?route=product/compare&lang_id={aLangId}',
                'history':  f'/?route=product/history&lang_id={aLangId}',
                'favorite': f'/?route=product/favorite&lang_id={aLangId}',
                'root': f'/?lang_id={aLangId}&country_id={aCountryId}'
            },
            'search': aSearch,
            'lang_id': aLangId,
            'country_id': aCountryId,
            'country': Country,
            'dbl_country': DblCountry.Export(),
            'now_year': datetime.now().year
        }
        return Res
