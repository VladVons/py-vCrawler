#https://tamethebots.com/tools/robotstxt-checker

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
    from Task.Crawler.Lib import InitRobots

    CustomRobots = '''
        Disallow: */filter/
        Disallow: */filter2/
    '''
    # Url = '/c600240/c637000/c663700/p685662.html?sort=p.price&order=ASC'
    # Url = 'http://oster.com.ua/c600240/c637000/c663700/p685662.html?sort=p.price&order=ASC'
    # Url = 'http://oster.com.ua/index.php/?route=account/login'
    # Url = 'http://oster.com.ua/index.php?route=account1/login&key=1'
    # Url = 'https://ktc.ua/search/?q=AirPods&t=d5e1fef75154b1ace345fd3fdbcc2279'
    # Url = 'https://telemart.ua/ua/monitors/filter/5120-2880px'
    Url = 'https://telemart.ua/ua/monitors/filter/'
    Robots = await InitRobots(Url, CustomRobots)
    q1 = Robots.can_fetch(Url, '*')
    print('done')


#Test2()
asyncio.run(ATest2())
print('done')
