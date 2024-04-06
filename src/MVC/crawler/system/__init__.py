# Created: 2024.04.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from urllib.parse import urlparse
from Inc.Misc.ClientSession import TDownloadSpeed


async def GetDownloadSpeed(self, aUrl: str) -> dict:
    Url = urlparse(aUrl)
    async with TDownloadSpeed(f'{Url.scheme}://{Url.hostname}', 2) as DS:
        return await DS.Test(Url.path)
