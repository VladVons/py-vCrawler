import aiohttp
import asyncio

# Your Ukrainian proxy URL (replace with actual proxy)
PROXY = "http://91.228.13.79:50100"
PROXY = "http://195.178.134.35:50100"
PROXY_USER = "vladvons"
PROXY_PASS = "Mc6bVJCgvo"
auth = aiohttp.BasicAuth(PROXY_USER, PROXY_PASS)

async def fetch(session, url):
    try:
        async with session.get(url, proxy=PROXY, proxy_auth=auth) as response:
            html = await response.text()
            print(f"{url}, status {response.status}")
            return html
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

async def crawl(urls):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            if (not url.startswith('-')):
                tasks.append(fetch(session, url))
        results = await asyncio.gather(*tasks)
        return results

if __name__ == "__main__":
    urls1 = [
        "-https://it.findwares.com",
        "-https://pc.com.ua/ua/acer-b223w-b",
        "https://laptop-planet.com.ua/lenovo-thinkpad-e14-14-fullhd-i5-10210u-16gb-ram-256gb-nvme/"
    ]
    asyncio.run(crawl(urls1))
