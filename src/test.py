import asyncio
from Inc.Misc.Cache import TCacheFile



async def Main():
    Cache = TCacheFile('/tmp/crawler/url')
    Cache.Clear()
    Url = 'https://acomp.com.ua/ua/kompyuter-dell-3020-i3-41308gb1tbssd-120gb-desktop-bu/'
    #Cache.Get(Url, {'emul': True})
    await Cache.Get(Url, {'emul': True})
    pass

asyncio.run(Main())
