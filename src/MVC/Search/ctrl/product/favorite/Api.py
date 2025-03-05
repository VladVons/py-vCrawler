# Created: 2025.01.10
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibCtrl as Lib
from ..._inc.products import List

class TMain(Lib.TCtrlBase):
    async def Main(self, **aData: dict) -> dict:
        aLangId, aUrlIds = Lib.GetDictDefs(
            aData.get('query'),
            ('lang_id', 'url_ids'),
            (1, '1,2,3')
        )

        Res = await List(self, aLangId, aUrlIds)
        Res['dbl_breadcrumbs'] = Lib.DblGetBreadcrumbs([['favorite', '']])
        return Res
