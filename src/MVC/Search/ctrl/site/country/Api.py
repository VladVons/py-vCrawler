# Created: 2024.11.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibCtrl as Lib


class TMain(Lib.TCtrlBase):
    async def Main(self, **aData):
        _aLangId, aCountryId = Lib.GetDictDefs(
            aData.get('query'),
            ('lang_id', 'country_id'),
            (1, 1)
        )

        DblCountry = await self.ExecModelImport(
            'site',
            {
                'method': 'GetCountryLangById',
                'param': {
                    'aCountryId': aCountryId
                }
            }
        )
        aLangId = DblCountry.Rec.GetField('lang_id', 1)

        DblSites = await self.ExecModelImport(
            'site',
            {
                'method': 'GetSiteCountry',
                'param': {
                    'aCountryId': aCountryId
                }
            }
        )

        DblSites.AddFieldsFill(['href'], False)
        for Rec in DblSites:
            Href = f'/?route=site/site&lang_id={aLangId}&site_id={Rec.id}'
            DblSites.RecMerge([Href])

        cntParsed = cntProducts = cntOnStock = cntDiscount = cntErr = 0
        for Rec in DblSites:
            if (Rec.products):
                cntParsed += 1
                cntProducts += Rec.products
                cntOnStock += Rec.onstock
                cntDiscount += Rec.discount
                cntErr += Rec.err

        if (self.GetConf('seo_url')):
            await Lib.SeoEncodeDbl(self, DblSites, ['href'])

        Res = {
            'dbl_sites': DblSites.Export(),
            'cnt_parsed': cntParsed,
            'cnt_products': cntProducts,
            'cnt_onstock': cntOnStock,
            'cnt_discount': cntDiscount,
            'cnt_err': cntErr,
            'cnt_all': len(DblSites),
            'href': {
                'btn': f'/?route=site/add&lang_id={aLangId}&country_id={aCountryId}'
            }
        }
        return Res
