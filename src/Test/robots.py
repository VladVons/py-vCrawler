#https://tamethebots.com/tools/robotstxt-checker

import asyncio
import json

def Test1():
    q1 = Robots.can_fetch('/c600240/c637000/c663700/p685662.html?sort=p.price&order=ASC', '*')
    q2 = Robots.can_fetch('http://oster.com.ua/c600240/c637000/c663700/p685662.html?sort=p.price&order=ASC', '*')
    q3 = Robots.can_fetch('http://oster.com.ua/index.php/?route=account/login', '*')
    q4 = Robots.can_fetch('http://oster.com.ua/index.php?route=account1/login&key=1', '*')

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

#Test2()
asyncio.run(ATest1())
print('done')
