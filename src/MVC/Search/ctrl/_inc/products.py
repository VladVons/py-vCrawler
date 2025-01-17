# Created: 2025.01.18
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from base64 import b64encode
from urllib.parse import quote
#
import IncP.LibCtrl as Lib


async def List(self, aLangId: int, aUrlIds: str, aReverse = False) -> dict:
    UrlIds = aUrlIds.split(',')
    if (not Lib.IsDigits(UrlIds)):
        return {'status_code': 404}

    UrlIds = list(map(int, UrlIds))
    if (aReverse):
        UrlIds.reverse()

    DblProducts = await self.ExecModelImport(
        'product',
        {
            'method': 'GetProductsAttrId',
            'param': {
                'aUrlIds': UrlIds
            }
        }
    )
    if (not DblProducts):
        return {'status_code': 404}

    Marker = 'findwares.com'
    Hash = quote(b64encode(Marker.encode()).decode('utf-8'))
    DblProducts.AddFieldsFill(['href', 'href_ext'], False)
    for Rec in DblProducts:
        Href = f'/?route=product/product&lang_id={aLangId}&url_id={Rec.url_id}'
        HrefExt = Rec.url + Lib.Iif('?' in Rec.url, '&', '?') + f'srsltid={Hash}'
        DblProducts.RecMerge([Href, HrefExt])

    if (self.GetConf('seo_url')):
        await Lib.SeoEncodeDbl(self, DblProducts, ['href'])

    return {
        'dbl_products': DblProducts.Export()
    }
