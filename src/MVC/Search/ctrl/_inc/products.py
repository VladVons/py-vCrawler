# Created: 2025.01.18
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

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

    Lib.DblProducts_Adjust(DblProducts, aLangId, self.GetConf('image_encrypt'))

    if (self.GetConf('seo_url')):
        await Lib.SeoEncodeDbl(self, DblProducts, ['href'])

    return {
        'dbl_products': DblProducts
    }
