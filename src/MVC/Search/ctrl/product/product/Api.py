# Created: 2024.11.21
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import json
#
from IncP.CtrlBase import TCtrlBase, Lib


class TMain(TCtrlBase):
    async def Main(self, **aData):
        aLang, aUrlId = Lib.GetDictDefs(
            aData.get('query'),
            ('lang', 'url_id'),
            ('ua', 0)
        )

        if (not Lib.IsDigits([aUrlId])):
            return {'status_code': 404}

        aLangId = 1
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
        Product['attr'] = DblProduct.Rec.attr

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

        Schema = {
            '@context': 'https://schema.org',
            '@type': 'Product',
            'image': Product.get('images'),
            'name': Product.get('name'),
            'description': Product.get('description'),
            'category': Product.get('category'),
            'brand': Product.get('brand'),
            'offers': {
                '@type': 'Offer',
                'availability': 'https://schema.org/' + Lib.Iif(Product.get('stock'), 'InStock', 'OutOfStock'),
                'price': Product.get('price')[0],
                'priceCurrency': Product.get('price')[1]
            }
        }
        Lib.DelValues(Schema, ['', [], {}, None])

        Res['schema'] = json.dumps(Schema, ensure_ascii=False)
        Res['product'] = Product
        Res['info'] = {
            'url_id': DblProduct.Rec.url_id
        }
        return Res
