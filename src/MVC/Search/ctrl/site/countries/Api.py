# Created: 2024.11.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.CtrlBase import TCtrlBase, Lib


class TMain(TCtrlBase):
    async def Main(self, **aData):
        aLangId = Lib.DeepGetByList(aData, ['query', 'lang'], 1)

        Dbl = await self.ExecModelImport(
            'site',
            {
                'method': 'GetSiteCountries',
                'param': {
                    'aLangId': aLangId
                }
            }
        )

        Hrefs = [f'/?route=site/country&country_id={Rec.country_id}' for Rec in Dbl]
        Dbl.AddFieldsFill(['href'], False)
        for Href, Rec in zip(Hrefs, Dbl):
            Dbl.RecMerge([Href])

        return {
            'dbl_countries': Dbl.Export()
        }
