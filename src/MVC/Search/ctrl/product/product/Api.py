# Created: 2024.11.21
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import json
#
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
                    'aUrlId': aUrlId,
                    'aLangId': aLangId
                }
            }
        )
        if (not DblProduct):
            return {'status_code': 404}

        Res = DblProduct.Rec.GetAsDict()
        ParsedData = DblProduct.Rec.parsed_data

        CountryId = DblProduct.Rec.country_id
        Attr = DblProduct.Rec.GetField('attr', {})
        DblAttr = Lib.TDbList(['key', 'val', 'href'])
        Category = Attr.get('category')
        for xKey, xVal in sorted(Attr.items()):
            Filter = f"f_category={Category}"
            if (xKey != 'category'):
                Filter += f'&f_{xKey}={xVal}'

            Href = f'/?route=product/country&lang_id={aLangId}&country_id={CountryId}&{Filter}'
            DblAttr.RecAdd([xKey, xVal, Href])


        # Similar products
        AttrSimilar = Attr.copy()
        Lib.DelKeys(AttrSimilar, ['model', 'brand', 'grade', 'storage/type', 'cpu/gen_short']) # 'screen_resol'
        DblProducts = await self.ExecModelImport(
            'product',
            {
                'method': 'GetProductsAttrCountry',
                'param': {
                    'aCountryId': CountryId,
                    'aFilter': AttrSimilar,
                    'aOrder': 'random()',
                    'aLimit': 10,
                    'aOffset': 0
                }
            }
        )

        if (DblProducts) and (not Lib.IsBot(aData['user_agent'])):
            Lib.DblProducts_Adjust(DblProducts, aLangId, self.GetConf('image_encrypt'))

            if (self.GetConf('seo_url')):
                await Lib.SeoEncodeDbl(self, DblProducts, ['href', 'href_int'])
            Res['dbl_products'] = DblProducts


        if ('brand' not in ParsedData):
            ParsedData['brand'] = ''

        if ('features' not in ParsedData):
            ParsedData['features'] = {}

        if ('image' not in ParsedData):
            ParsedData['image'] = 'http://someurl.img'

        if ('images' not in ParsedData):
            ParsedData['images'] = []
            if ('image' in ParsedData):
                ParsedData['images'].append(ParsedData['image'])

        if ('price' not in ParsedData):
            ParsedData['price'] = [0, '']

        if ('stock' not in ParsedData):
            ParsedData['stock'] = False

        if (self.GetConf('image_encrypt')):
            ParsedData['image'] = Lib.ImgProxy(ParsedData['image'])
            for Idx, xImage in enumerate(ParsedData['images']):
                ParsedData['images'][Idx] = Lib.ImgProxy(xImage)

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
            'image': ParsedData.get('images'),
            'name': ParsedData.get('name'),
            'description': ParsedData.get('description'),
            'category': Attr.get('category'),
            'model': Attr.get('model'),
            'brand': Attr.get('brand'),
            'offers': {
                '@type': 'Offer',
                'availability': 'https://schema.org/' + Lib.Iif(ParsedData.get('stock'), 'InStock', 'OutOfStock'),
                'price': ParsedData.get('price')[0],
                'priceCurrency': ParsedData.get('price')[1]
            },
            'additionalProperty': AttrSchema
        }
        Lib.DelValues(Schema, ['', [], {}, None])

        Tabs = {
            'features': bool(ParsedData.get('features')),
            'details': bool(ParsedData.get('description'))
        }
        TabActive = Lib.DictFindVal(Tabs, True, 'features')

        if (self.GetConf('seo_url')):
            await Lib.SeoEncodeDbl(self, DblAttr, ['href'])

        Res['dbl_attr'] = DblAttr
        Res['parsed_data'] = ParsedData

        ResExt = {
            'schema': json.dumps(Schema, ensure_ascii=False, indent=1),
            'meta_title': ParsedData['name'],
            'meta_image': ParsedData['image'],
            'url_id': aUrlId,
            'category': Category,
            'price': ParsedData.get('price')[0],
            'host': Lib.UrlToDict(DblProduct.Rec.site_url)['host'],
            'tab_active': TabActive,
            'href': {
                'site': f'/?route=site/site&lang_id={aLangId}&site_id={DblProduct.Rec.site_id}',
                'category': f'/?route=product/country&lang_id={aLangId}&country_id={CountryId}&f_category={Category}'
            }
        }
        Res.update(ResExt)
        return Res
