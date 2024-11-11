# Created: 2024.04.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from base64 import b64encode
from urllib.parse import quote
from IncP.CtrlBase import TCtrlBase, Lib


class TMain(TCtrlBase):
    async def Main(self, **aData):
        aSearch, aCountryId, aSort, aOrder, aPage, aLimit = Lib.GetDictDefs(
            aData.get('query'),
            ('q', 'country_id', 'sort', 'order', 'page', 'limit'),
            ('', 1, ('sort_order, title', 'title', 'price', 'stock'), ('asc', 'desc'), 1, 10)
        )

        aLimit = min(aLimit, 25)

        if (not Lib.IsDigits([aPage, aLimit])):
            return {'status_code': 404}

        DblProducts = await self.ExecModelImport(
            'product',
            {
                'method': 'Get_Products_Search2',
                'param': {
                    'aFilter': aSearch,
                    'aCountryId': aCountryId,
                    'aOrder': f'{aSort} {aOrder}',
                    'aLimit': aLimit,
                    'aOffset': (aPage - 1) * aLimit
                }
            }
        )

        if (not DblProducts):
            DblProducts = await self.ExecModelImport(
                'product',
                {
                    'method': 'Get_Products_Search1',
                    'param': {
                        'aFilter': aSearch,
                        'aCountryId': aCountryId,
                        'aOrder': f'{aSort} {aOrder}',
                        'aLimit': aLimit,
                        'aOffset': (aPage - 1) * aLimit
                    }
                }
            )

        Res = {}
        if (not DblProducts):
            Res['status_code'] = 404
            return Res

        Marker = 'findwares.com'
        Hash = quote(b64encode(Marker.encode()).decode('utf-8'))
        DblProducts.ToList()
        for Rec in DblProducts:
            Url = Rec.url
            Url = Url + Lib.Iif('?' in Url, '&', '?') + f'srsltid={Hash}'
            Rec.SetField('url', Url)

        Pagination = Lib.TPagination(aLimit, aData['path_qs'])
        Pagination.Visible = 7
        PData = Pagination.Get(DblProducts.Rec.total, aPage)
        DblPagination = Lib.TDbList(['page', 'title', 'href', 'current'], PData)

        Res['dbl_products'] = DblProducts.Export()
        Res['dbl_pagenation'] = DblPagination.Export()
        return Res
