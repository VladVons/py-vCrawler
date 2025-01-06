# Created: 2024.12.19
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibCtrl as Lib

class TMain(Lib.TCtrlBase):
    async def Main(self, **aData):
        aSiteId, aLangId = Lib.GetDictDefs(
            aData.get('query'),
            ('site_id', 'lang_id'),
            (1, 1)
        )

        if (not Lib.IsDigits([aSiteId, aLangId])):
            return {'status_code': 404}

        DblInfo = await self.ExecModelImport(
            'site',
            {
                'method': 'GetSiteInfo',
                'param': {
                    'aSiteId': aSiteId,
                    'aLangId': aLangId
                }
           }
        )
        if (not DblInfo):
            return {'status_code': 404}

        DblCategories = await self.ExecModelImport(
            'site',
            {
                'method': 'GetSiteCategories',
                'param': {
                    'aSiteId': aSiteId
                }
           }
        )

        DblCategories.AddFieldsFill(['href'], False)
        for Rec in DblCategories:
            Href = f'/?route=product/site&lang_id={aLangId}&site_id={aSiteId}&f_category={Rec.category}'
            DblCategories.RecMerge([Href])

        if (self.ApiCtrl.ConfDb.get('seo_url')):
            await Lib.SeoEncodeDbl(self, DblCategories, 'href')

        Res = DblInfo.Rec.GetAsDict()
        Res['host'] = Lib.UrlToDict(Res['url'])['host']
        Res['dbl_categories'] = DblCategories.Export()
        return Res
