import asyncio
from Inc.Misc.Sitemap import TSitemapRead

async def Main():
    Sitemap = TSitemapRead('https://chipchip.ua/ua')
    Urls = await Sitemap.Load()
    pass

asyncio.run(Main())
