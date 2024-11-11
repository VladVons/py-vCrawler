# Created: 2024.11.11
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.CtrlBase import TCtrlBase, Lib

class TMain(TCtrlBase):
    async def Main(self, **aData) -> dict:
        aSearch, aCountryId = Lib.GetDictDefs(
            aData.get('query'),
            ('q', 'country_id'),
            ('', 1)
        )

        DblCountry = await self.ExecModelImport(
            'site',
            {
                'method': 'GetCountries',
                'param': {}
            }
        )

        Href = {
            'counties': '/?route=site/countries'
        }

        return  {
            'href': Href,
            'search': aSearch,
            'country_id': aCountryId,
            'dbl_country': DblCountry.Export()
        }
