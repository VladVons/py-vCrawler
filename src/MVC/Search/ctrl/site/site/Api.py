# Created: 2024.12.19
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Misc.Crypt import GetCRC
import IncP.LibCtrl as Lib

class TMain(Lib.TCtrlBase):
    async def Main(self, **aData):
        aLangId, aSiteId = Lib.GetDictDefs(
            aData.get('query'),
            ('lang_id', 'site_id'),
            (1, 1)
        )

        if (not Lib.IsDigits([aSiteId, aLangId])):
            return {'status_code': 404}

        DblInfo = await self.ExecModelImport(
            'site',
            {
                'method': 'GetSiteInfo',
                'param': {
                    'aLangId': aLangId,
                    'aSiteId': aSiteId
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

        Res = DblInfo.Rec.GetAsDict()
        if (self.GetConf('seo_url')):
            await Lib.SeoEncodeDbl(self, DblCategories, ['href'])

        Res['host'] = Lib.UrlToDict(Res['url'])['host']
        Res['dbl_categories'] = DblCategories.Export()
        Res['href'] = {
            'host': f'/?route=redirect&{Lib.GetRedirectHref(Res['url'])}'
        }
        return Res
