# Created: 2024.11.21
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import json
#
from Inc.Http.HttpUrl import UrlToDict
import IncP.LibCtrl as Lib


class TMain(Lib.TCtrlBase):
    async def Main(self, **aData):
        aLangId, aUrlId = Lib.GetDictDefs(
            aData.get('query'),
            ('lang_id', 'url_id'),
            (1, 0)
        )

        DblProduct = await self.ExecModelImport(
            'product',
            {
                'method': 'GetProductByUrlId',
                'param': {
                    'aUrlId': aUrlId
                }
            }
        )
        if (not DblProduct):
            return {'status_code': 404}

        Res = {}
        Product = DblProduct.Rec.product

        CountryId = DblProduct.Rec.country_id
        Attr = DblProduct.Rec.GetField('attr', {})
        DblAttr = Lib.TDbList(['key', 'val', 'href'])
        for xKey, xVal in sorted(Attr.items()):
            Filter = f"f_category={Attr.get('category')}"
            if (xKey != 'category'):
                Filter += f'&f_{xKey}={xVal}'

            Href = f'/?route=product/category&lang_id={aLangId}&country_id={CountryId}&{Filter}'
            DblAttr.RecAdd([xKey, xVal, Href])

        if ('brand' not in Product):
            Product['brand'] = ''

        if ('features' not in Product):
            Product['features'] = {}

        if ('image' not in Product):
            Product['image'] = 'http://someurl.img'

        if ('images' not in Product):
            Product['images'] = []

        if ('price' not in Product):
            Product['price'] = [0, '']

        if ('stock' not in Product):
            Product['stock'] = False

        AttrSchema = [
            {
                '@type': 'PropertyValue',
                'name': xKey,
                'value': xVal
            }
            for xKey, xVal in Attr.items()
        ]

        Schema = {
            '@context': 'https://schema.org',
            '@type': 'Product',
            'image': Product.get('images'),
            'name': Product.get('name'),
            'description': Product.get('description'),
            'category': Attr.get('category'),
            'model': Attr.get('model'),
            'brand': Attr.get('brand'),
            'offers': {
                '@type': 'Offer',
                'availability': 'https://schema.org/' + Lib.Iif(Product.get('stock'), 'InStock', 'OutOfStock'),
                'price': Product.get('price')[0],
                'priceCurrency': Product.get('price')[1]
            },
            'additionalProperty': AttrSchema
        }
        Lib.DelValues(Schema, ['', [], {}, None])

        if (self.GetConf('seo_url')):
            await Lib.SeoEncodeDbl(self, DblAttr, ['href'])

        Res = {
            'dbl_attr': DblAttr.Export(),
            'product': Product,
            'schema': json.dumps(Schema, ensure_ascii=False, indent=1),
            'meta_title': Product['name'],
            'meta_image': Product['image'],
            'href': {
                'site': f'/?route=site/site&lang_id={aLangId}&site_id={DblProduct.Rec.site_id}'
            },
            'url_id': DblProduct.Rec.url_id,
            'url': DblProduct.Rec.url,
            'host': UrlToDict(DblProduct.Rec.url)['host']
        }
        return Res
