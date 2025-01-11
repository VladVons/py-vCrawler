# Created: 2025.01.08
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibCtrl as Lib


class TMain(Lib.TCtrlBase):
    async def Main(self, **aData: dict) -> dict:
        aLangId, aUrlIds  = Lib.GetDictDefs(
            aData.get('query'),
            ('lang_id', 'url_ids'),
            (1, '1,2,3')
        )

        MaxLen = 6
        UrlIds = aUrlIds.split(',')[:MaxLen]
        if (not Lib.IsDigits(UrlIds)):
            return {'status_code': 404}

        Dbl = await self.ExecModelImport(
            'product',
            {
                'method': 'GetProductByUrlIds',
                'param': {
                    'aUrlIds': UrlIds
                }
            }
        )
        if (not Dbl):
            return {'status_code': 404}

        AttrKeys = []
        for Rec in Dbl:
            if (Rec.attr):
                AttrKeys += Rec.attr.keys()
        ProductKeys = ['image', 'name', 'price']
        Fields = ProductKeys + sorted(set(AttrKeys))

        DblCompare = Lib.TDbList(['url_id', 'href'] + Fields)
        for Rec in Dbl:
            RecNew = DblCompare.RecAdd()
            RecNew.SetField('url_id', Rec.url_id)
            Href = f'/?route=product/product&lang_id={aLangId}&url_id={Rec.url_id}'
            RecNew.SetField('href', Href)

            FastProduct = Rec.product
            for xKey in ProductKeys:
                RecNew.SetField(xKey, FastProduct.get(xKey))

            for xKey, xVal in Rec.attr.items():
                RecNew.SetField(xKey, xVal)

        if (self.GetConf('seo_url')):
            await Lib.SeoEncodeDbl(self, DblCompare, 'href')

        Res = {
            'dbl_compare': DblCompare.Export(),
            'rows': Fields
        }
        return Res
