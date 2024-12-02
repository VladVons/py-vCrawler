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

        Dbl = Lib.TDbList().Import(DblData)
        cntParsed = cntProducts = cntOnStock = cntDiscount = cntErr = 0
        for Rec in Dbl:
            if (Rec.products):
                cntParsed += 1
                cntProducts += Rec.products
                cntOnStock += Rec.onstock
                cntDiscount += Rec.discount
                cntErr += Rec.err

        return {
            'dbl_sites': DblData,
            'cnt_parsed': cntParsed,
            'cnt_products': cntProducts,
            'cnt_onstock': cntOnStock,
            'cnt_discount': cntDiscount,
            'cnt_err': cntErr,
            'cnt_all': len(Dbl)
        }
