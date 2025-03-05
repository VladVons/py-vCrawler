# Created: 2025.01.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibCtrl as Lib


class TMain(Lib.TCtrlBase):
    async def Main(self, **aData):
        aPage, aLimit, aHaving = Lib.GetDictDefs(
            aData.get('query'),
            ('page', 'limit', 'having'),
            (1, 50, 0)
        )

        if (not Lib.IsDigits([aPage, aLimit, aHaving])):
            return {'status_code': 404}

        DblMain = await self.ExecModelImport(
            'tools',
            {
                'method': 'Get_HistSession',
                'param': {
                    'aLimit': aLimit,
                    'aOffset': (aPage - 1) * aLimit,
                    'aHaving': aHaving
                }
            }
        )
        if (not DblMain):
            return

        Href = aData['path_qs']
        #Href = UrlEncode(aData['query'])

        Pagination = Lib.TPagination(aLimit, Href)
        PData = Pagination.Get(DblMain.Rec.total, aPage)
        DblPagination = Lib.TDbList(['page', 'title', 'href', 'current'], PData)

        DblDay = await self.ExecModelImport(
            'tools',
            {
                'method': 'Get_HistUniqIpPerDay',
                'param': {
                    'aLimit': 360//2,
                    'aOffset': 0
                }
            }
        )

        Res = {
            'dbl_main': DblMain,
            'dbl_pagenation': DblPagination,
            'day_inf': DblDay.ExportPairs('create_day', ['count', 'count_id', 'count_url', 'count_ip', 'count_location'], True)
        }
        return Res
