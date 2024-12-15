# Created: 2024.04.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.CtrlBase import TCtrlBase, Lib

class TMain(TCtrlBase):
    async def Main(self, **aData):
        aCountryId, = Lib.GetDictDefs(
            aData.get('query'),
            ('country_id', ),
            (1, )
        )

        DblCategory = await self.ExecModelImport(
            'category',
            {
                'method': 'GetCountryCategories',
                'param': {
                    'aCountryId': aCountryId
                },
                'cache_age': 60*10
            }
        )

        Trans = await self.Translate('ua', DblCategory.ExportList('category'))
        Lib.DblTranslate(DblCategory, 'category', Trans)

        return {
            'dbl_category': DblCategory.Export()
        }
