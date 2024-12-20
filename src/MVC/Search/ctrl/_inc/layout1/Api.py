# Created: 2024.11.11
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.CtrlBase import TCtrlBase, Lib

class TMain(TCtrlBase):
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
                'param': {}
            }
        )

        Href = {
            'counties': f'/?route=site/countries&lang_id={aLangId}'
        }

        return  {
            'href': Href,
            'search': aSearch,
            'country_id': aCountryId,
            'dbl_country': DblCountry.Export()
        }
