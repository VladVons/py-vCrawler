# Created: 2024.04.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.CtrlBase import TCtrlBase, Lib


class TMain(TCtrlBase):
    async def Main(self, aData: dict):
        aSearch, aSort, aOrder, aPage, aLimit = Lib.GetDictDefs(
            aData.get('query'),
            ('q', 'sort', 'order', 'page', 'limit'),
            ('', ('sort_order, title', 'title', 'price'), ('asc', 'desc'), 1, 10)
        )

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

            if (not Dbl):
                return {'status_code': 404}

        Pagination = Lib.TPagination(aLimit, aData['path_qs'])
        PData = Pagination.Get(Dbl.Rec.total, aPage)
        DblPagination = Lib.TDbList(['page', 'title', 'href', 'current'], PData)

        return {
            'dbl_products': Dbl.Export(),
            'dbl_pagenation': DblPagination.Export(),
            'search': aSearch
        }
