# Created: 2024.11.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.CtrlBase import TCtrlBase, Lib


class TMain(TCtrlBase):
    async def Main(self, **aData):
        aLangId, aCountryId, aLimit = Lib.GetDictDefs(
            aData.get('query'),
            ('lang_id', 'country_id', 'limit'),
            (1, 1, 100)
        )

        Dbl = await self.ExecModelImport(
            'site',
            {
                'method': 'GetSiteCountry',
                'param': {
                    'aCountryId': aCountryId
                }
            }
        )

        Dbl.AddFieldsFill(['href'], False)
        for Rec in Dbl:
            Href = f'/?route=site/site&lang_id={aLangId}&site_id={Rec.id}'
            Dbl.RecMerge([Href])

        cntParsed = cntProducts = cntOnStock = cntDiscount = cntErr = 0
        for Rec in Dbl:
            if (Rec.products):
                cntParsed += 1
                cntProducts += Rec.products
                cntOnStock += Rec.onstock
                cntDiscount += Rec.discount
                cntErr += Rec.err

        Res = {
            'dbl_sites': Dbl.Export(),
            'cnt_parsed': cntParsed,
            'cnt_products': cntProducts,
            'cnt_onstock': cntOnStock,
            'cnt_discount': cntDiscount,
            'cnt_err': cntErr,
            'cnt_all': len(Dbl)
        }
        return Res
