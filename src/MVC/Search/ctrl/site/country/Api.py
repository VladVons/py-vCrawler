# Created: 2024.11.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.CtrlBase import TCtrlBase, Lib


class TMain(TCtrlBase):
    async def Main(self, **aData):
        aCountryId, aLimit = Lib.GetDictDefs(
            aData.get('query'),
            ('country_id', 'limit'),
            (1, 100)
        )

        DblData = await self.ExecModel(
            'site',
            {
                'method': 'GetSiteCountry',
                'param': {
                    'aCountryId': aCountryId
                }
            }
        )

        return {
            'dbl_sites': DblData
        }