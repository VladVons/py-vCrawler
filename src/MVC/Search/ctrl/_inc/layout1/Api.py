# Created: 2024.11.11
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from datetime import datetime
#
import IncP.LibCtrl as Lib
from IncP import GetAppVer

class TMain(Lib.TCtrlBase):
    async def Main(self, **aData) -> dict:
        aLangId, aCountryId = Lib.GetDictDefs(
            aData.get('query'),
            ('lang_id', 'country_id'),
            (1, 1)
        )

        DblCategories = await Lib.DblGetCategories(self, aLangId, aCountryId, 'country')
        if (self.GetConf('seo_url')):
            await Lib.SeoEncodeDbl(self, DblCategories, ['href'])

        Href = {
            'about_us': f'/?route=info/about_us&lang_id={aLangId}',
            'add_site': f'/?route=common/add_site&lang_id={aLangId}',
            'compare':  f'/?route=product/compare&lang_id={aLangId}',
            'contact_us': f'/?route=common/contact_us&lang_id={aLangId}',
            'countries': f'/?route=site/countries&lang_id={aLangId}',
            'history':  f'/?route=product/history&lang_id={aLangId}',
            'favorite': f'/?route=product/favorite&lang_id={aLangId}',
            'privacy_policy': f'/?route=info/privacy_policy&lang_id={aLangId}',
            'root': f'/?lang_id={aLangId}&country_id={aCountryId}'
        }

        AppVer = GetAppVer()
        Res = {
            'dbl_categories': DblCategories,
            'href_search_ajax': '/api/?route=product/search',
            'href': Href,
            'now_year': datetime.now().year,
            'ver': f"ver:{AppVer['app_ver']} ({AppVer['app_date']})"
        }
        return Res
