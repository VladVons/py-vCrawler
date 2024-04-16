# Created: 2024.04.15
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import re
import gzip
import asyncio
from urllib.parse import urlparse
import aiohttp
from bs4 import BeautifulSoup
from protego import Protego
#
from Inc.Util.Obj import GetTree


def GetSoup(aData: str) -> BeautifulSoup:
    Res = BeautifulSoup(aData, 'lxml')
    if (len(Res) == 0):
        Res = BeautifulSoup(aData, 'html.parser')
    return Res

def EscForSQL(aData: dict):
    for _Nested, _Path, Obj, _Depth in GetTree(aData):
        if (isinstance(Obj, dict)):
            for Key in Obj:
                if (isinstance(Obj[Key], str)) and ("'" in Obj[Key]):
                    Obj[Key] = Obj[Key].replace("'", "''")

def IsMimeApp(aUrl: str) -> bool:
    Path = urlparse(aUrl).path
    Ext = os.path.splitext(Path)[1].lower()
    if (Ext == '' or Ext in ['.php']):
        Res = False
    else:
        Mime = [
            '.zip', '.rar', '.7z', '.gz', '.bz',
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.ico',
            '.wav', '.mp3', '.mp4', '.mpeg',
            '.xml', '.pdf', '.doc', '.docx', '.xls', '.xlsx'
        ]
        Res = (Ext in Mime)
    return Res

async def GetUrlData(aUrl: str) -> object:
    async def _GetUrlData(aHeaders: dict):
        async with aiohttp.ClientSession() as Session:
            try:
                async with Session.get(aUrl, headers=aHeaders) as Response:
                    Data = await Response.read()
                    Res = {'data': Data, 'status': Response.status}
            except Exception as E:
                Res = {'err': str(E), 'status': -1}
            return Res

    Headers = [
        {
            'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'Accept-Language': 'uk'
        },
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
            'Accept-Language': 'uk'
        }
    ]

    for xHeader in Headers:
        Res = await _GetUrlData(xHeader)
        if (Res['status'] != 403):
            break
        await asyncio.sleep(0.5)
    return Res



async def InitRobots(aUrl: str, aCustom: str) -> Protego:
    Parsed = urlparse(aUrl)
    Url = f'{Parsed.scheme}://{Parsed.hostname}/robots.txt'
    UrlData = await GetUrlData(Url)
    Content = ''
    if (UrlData['status'] == 200):
        Content = UrlData['data'].decode()
        if (aCustom):
            Lines = Content.splitlines()
            ArrAgent = (i for i, line in enumerate(Lines) if line.strip() == 'User-agent: *')
            Idx = next(ArrAgent, None)
            if (Idx is not None):
                Lines.insert(Idx + 1, aCustom + '\n')
                Content = '\n'.join(Lines)
    return Protego.parse(content=Content)

RE_cdata = re.compile(r'<!\[CDATA\[(.*?)\]\]>', re.IGNORECASE)
async def LoadSiteMap(aUrl: str) -> list:
    Res = []

    UrlData = await GetUrlData(aUrl)
    if (UrlData['status'] == 200):
        Data = UrlData['data']
        if (aUrl.endswith('.xml.gz')):
            Data = gzip.decompress(Data)

        Data = Data.decode()
        Urls = re.findall('<loc>(.*?)</loc>', Data)
        for Url in Urls:
            if (Url.endswith('.xml')) or (Url.endswith('.xml.gz')):
                Res += await LoadSiteMap(Url)
            else:
                if ('CDATA' in Url):
                    Match = RE_cdata.match(Url)
                    Url = Match.group(1)

                if (not IsMimeApp(Url)):
                    Res.append(Url.rstrip('/'))
    return Res
