# Created: 2024.04.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.CtrlBase import TCtrlBase, Lib

class TMain(TCtrlBase):
    async def Main(self, aData: dict):
        aSearch, aSort, aOrder, aPage, aLimit = Lib.GetDictDefs(
            aData.get('query'),
            ('q', 'sort', 'order', 'page', 'limit'),
            ('', ('sort_order, title', 'title', 'price'), ('asc', 'desc'), 1, 25)
        )

        if (not Lib.IsDigits([aPage, aLimit])):
            return {'status_code': 404}

        Dbl = await self.ExecModelImport(
            'product',
            {
                'method': 'Get_Products_Search',
                'param': {
                    'aFilter': aSearch,
                    'aOrder': f'{aSort} {aOrder}',
                    'aLimit': aLimit,
                    'aOffset': (aPage - 1) * aLimit
                }
            }
        )
        if (Dbl):
            pass

        return {'t2': 1234}
