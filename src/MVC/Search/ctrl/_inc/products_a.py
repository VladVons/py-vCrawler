# Created: 2025.01.10
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibCtrl as Lib


async def Main(self, aDbl: Lib.TDbList) -> Lib.TDbList:
    Missed = aDbl.Rec.GetFieldsMissed(['image', 'url_id'])
    assert (not Missed), f'Missed fields {Missed}'

    Hrefs = []
    for Rec in aDbl:
        Hrefs.append(f'/?route=product0/product&product_id={Rec.product_id}')
        Hrefs.append(f'/?route=product0/category&category_id={Rec.category_id}')

    if (self.ApiCtrl.Conf.get('seo_url')):
        Hrefs = await Lib.SeoEncodeList(self, Hrefs)

    PartSize = len(Hrefs) // len(aDbl)
    aDbl.AddFieldsFill(['thumb', 'product_href', 'category_href', 'tenant_href'], False)
    Zip = zip(ResThumbs['thumb'], aDbl, strict=True)
    for Idx, (Thumb, Rec) in enumerate(Zip):
        Idx = Idx * PartSize
        Parts = Hrefs[Idx:Idx+PartSize]
        New = [Thumb] + Parts
        aDbl.RecMerge(New)
    return aDbl