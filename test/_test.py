#https://tamethebots.com/tools/robotstxt-checker

# import sys
# sys.path.append('../src')

import asyncio
import json


def Test2():
    import json
    from Inc.Util.Obj import GetTree

    with open('kts.json', 'r') as F:
        ParsedData = json.load(F)
    print(ParsedData)

async def ATest1():
    from Task.Crawler.Lib import LoadSiteMap

    #Res1 = await LoadSiteMap('https://fozzyshop.ua/sitemap.xml')
    #Res1 = await LoadSiteMap('http://oster.com.ua/sitemap.xml')
    Res1 = await LoadSiteMap('https://telemart.ua/sitemap.xml')
    with open('sitemap.json', 'w') as F:
        json.dump(Res1, F, indent=1, ensure_ascii=False)

async def ATest2():
    from Task.Collector.Crawler.Lib import InitRobots

    CustomRobots = '''
        Disallow: *inCartProductId
    '''
    # Url = 'http://oster.com.ua/c600240/c637000/c663700/p685662.html?sort=p.price&order=ASC'
    # Url = 'http://oster.com.ua/index.php/?route=account/login'
    # Url = 'https://ktc.ua/search/?q=AirPods&t=d5e1fef75154b1ace345fd3fdbcc2279'
    # Url = 'https://telemart.ua/ua/monitors/filter/5120-2880px'
    # Url = 'https://telemart.ua/ua/monitors/filter/'
    # Url = 'https://www.moyo.ua/ua/news/kak_sbrosit_printer_do_zavodskikh_nastroek_canon_i_eshche_2_varianta_obnuleniya.html'
    # Url = 'https://brain.com.ua/ukr/category/Dirokoli-c2682/filter=7677-86017484100'
    # Url = 'https://ktc.ua/display_etc/brand-belkin/type-kabel/?page=3'
    # Url = 'https://exe.ua/ua?diagonal-monitora-235[0]=9477&sort=price&order=asc'
    # Url = 'https://exe.ua/ua/category/c33158/?page=14&lang=r1u'
    # Url = 'https://exe.ua/ua/category/c4102/_sovmestimost-wc-5024-f8218-v65188'
    Url = 'https://laptopchik.top/catalog?inCartProductId=14754'

    Robots = await InitRobots(Url, CustomRobots)
    CanFetch = Robots.can_fetch(Url, '*')
    print('CanFetch', CanFetch)
    print('done')

async def ATest3():
    from Task.Collector.Crawler.Lib import GetUrlData

    Url = 'https://brain.com.ua/ukr/category/Videokarty-c1403'
    UrlData = await GetUrlData(Url)
    print('done')

async def ATest4():
    from urllib.parse import urljoin

    base_url = 'https://telemart.ua/ua/'
    path = '?ua/akusticheskie-sistemy'
    result = urljoin(base_url, path)
    print(result)

#Test2()
asyncio.run(ATest2())
print('done')
