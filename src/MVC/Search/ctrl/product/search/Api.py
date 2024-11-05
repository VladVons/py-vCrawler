# Created: 2024.04.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from base64 import b64encode
from urllib.parse import quote
from IncP.CtrlBase import TCtrlBase, Lib


class TMain(TCtrlBase):
    async def Main(self, **aData):
        aSearch, aSort, aOrder, aPage, aLimit = Lib.GetDictDefs(
            aData.get('query'),
            ('q', 'sort', 'order', 'page', 'limit'),
            ('', ('sort_order, title', 'title', 'price', 'stock'), ('asc', 'desc'), 1, 10)
        )

        aLimit = min(aLimit, 25)

        if (not Lib.IsDigits([aPage, aLimit])):
            return {'status_code': 404}

        Dbl = await self.ExecModelImport(
            'product',
            {
                'method': 'Get_Products_Search2',
                'param': {
                    'aFilter': aSearch,
                    'aOrder': f'{aSort} {aOrder}',
                    'aLimit': aLimit,
                    'aOffset': (aPage - 1) * aLimit
                }
            }
        )

        if (not Dbl):
            Dbl = await self.ExecModelImport(
                'product',
                {
                    'method': 'Get_Products_Search1',
                    'param': {
                        'aFilter': aSearch,
                        'aOrder': f'{aSort} {aOrder}',
                        'aLimit': aLimit,
                        'aOffset': (aPage - 1) * aLimit
                    }
                }
            )

        Res = {'search': aSearch}
        if (not Dbl):
            Res['status_code'] = 404
            return Res

        Marker = 'findwares.com'
        Hash = quote(b64encode(Marker.encode()).decode('utf-8'))
        Dbl.ToList()
        for Rec in Dbl:
            Url = Rec.url
            Url = Url + Lib.Iif('?' in Url, '&', '?') + f'srsltid={Hash}'
            Rec.SetField('url', Url)

        Pagination = Lib.TPagination(aLimit, aData['path_qs'])
        Pagination.Visible = 7
        PData = Pagination.Get(Dbl.Rec.total, aPage)
        DblPagination = Lib.TDbList(['page', 'title', 'href', 'current'], PData)

        Res['dbl_products'] = Dbl.Export()
        Res['dbl_pagenation'] = DblPagination.Export()
        return Res
