# Created: 2025.01.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibCtrl as Lib

class TMain(Lib.TCtrlBase):
    async def RegSession(self, aIp: str, aUAgent: str, aLocation: str) -> dict:
        return await self.ExecModel(
            'system',
            {
                'method': 'RegSession',
                'param': {
                    'aIp': aIp,
                    'aUAgent': aUAgent,
                    'aLocation': aLocation
                }
            }
        )

    async def GetLocales(self, aCountry: str) -> dict:
        #aCountry = 'poland'
        Dbl = await self.ExecModelImport(
            'site',
            {
                'method': 'GetCountryLangByName',
                'param': {
                    'aCountry': aCountry.strip()
                },
                'cache_age': -1
            }
        )

        if (Dbl):
            return (Dbl.Rec.lang_id, Dbl.Rec.country_id)

    async def OnExec(self, **aData: dict) -> dict:
        aLangId, aCountryId = Lib.GetDictDefs(
            aData.get('query'),
            ('lang_id', 'country_id'),
            (-1, -1)
        )

        if (aCountryId == -1):
            aCountryId = int(Lib.DeepGetByList(aData, ['session', 'keys', 'country_id'], -1))

        SessionId = Lib.DeepGetByList(aData, ['session', 'keys', 'session_id'])
        if (SessionId):
            await self.ExecModel(
                'system',
                {
                    'method': 'Ins_HistPageView',
                    'param': {
                        'aSessionId': SessionId,
                        'aUrl': aData['path_qs']
                    }
                }
            )

        Country = Lib.DeepGetByList(aData, ['session', 'location', 'country'])
        if (Country and aLangId == -1 and aCountryId == -1):
            Locales = await self.GetLocales(Country)
            if (Locales):
                aLangId, aCountryId = Locales

        aLangId = Lib.Iif(aLangId == -1, 1, aLangId)
        aCountryId = Lib.Iif(aCountryId == -1, 1, aCountryId)
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

        return {
            'country': Country,
            'dbl_country': DblCountry,
            'query': aData.get('query')
        }
