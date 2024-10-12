import asyncio
from Inc.Misc.aiohttpClient import UrlGetData


async def Main():
    Url = 'https://a-pc.com.ua/bv-mon-tori/mon-tor-22-philips-225pl2-1680-x-1050-tft-lcd-a-b-v'

    Data = await UrlGetData(Url)
    print("done")

asyncio.run(Main())
