# Created: 2024.11.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibCtrl as Lib


class TMain(Lib.TCtrlBase):
    async def Main(self, **aData):
        aLangId = Lib.DeepGetByList(aData, ['query', 'lang_id'], 1)

        DblCountries = await self.ExecModelImport(
            'site',
            {
                'method': 'GetSiteCountries',
                'param': {
                    'aLangId': aLangId
                }
            }
        )

        DblCountries.AddFieldsFill(['href'], False)
        for Rec in DblCountries:
            Href = f'/?route=site/country&lang_id={Rec.lang_id}&country_id={Rec.country_id}'
            DblCountries.RecMerge([Href])

        if (self.GetConf('seo_url')):
            await Lib.SeoEncodeDbl(self, DblCountries, ['href'])

        Res = {
            'dbl_countries': DblCountries
        }
        return Res
