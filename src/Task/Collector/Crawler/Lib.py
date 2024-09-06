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


def DictToCookie(aDict) -> str:
    return '; '.join([f'{Key}={Val}' for Key, Val in aDict.items()])

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
            '.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp', '.ico',
            '.wav', '.mp3', '.mp4', '.mpeg',
            '.xml', '.pdf', '.doc', '.docx', '.xls', '.xlsx'
        ]
        Res = (Ext in Mime)
    return Res

async def GetUrlData(aUrl: str, aHeaders: dict = None) -> object:
    Headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
        'Accept-Language': 'uk'
    }

    if (aHeaders):
        for Key, Val in aHeaders.items():
            if isinstance(Val, dict):
                Val = DictToCookie(Val)
            Headers[Key] = Val

    UrlP = urlparse(aUrl)
    UrlHost = '%s://%s' % (UrlP.scheme, UrlP.hostname)
    UrlPath = UrlP.path

    async with aiohttp.ClientSession(base_url=UrlHost, headers=Headers, max_field_size=16384) as Session:
        await asyncio.sleep(1)
        try:
            async with Session.get(UrlPath) as Response:
                await asyncio.sleep(1)
                Data = await Response.read()
                Res = {'data': Data, 'status': Response.status}
        except Exception as E:
            Res = {'err': str(E), 'status': -1}
    return Res

async def InitRobots(aUrl: str, aCustom: str = '') -> Protego:
    Parsed = urlparse(aUrl)
    Url = f'{Parsed.scheme}://{Parsed.hostname}/robots.txt'
    UrlData = await GetUrlData(Url)
    if (UrlData['status'] == 200):
        Content = UrlData['data'].decode()
    else:
        Content = ''

    if (aCustom):
        Lines = Content.splitlines()
        ArrAgent = (i for i, line in enumerate(Lines) if line.lower().strip() == 'user-agent: *')
        IdxPos = next(ArrAgent, None)
        if (IdxPos is None):
            Lines.append('user-agent: *')
            IdxPos = len(Lines)

        for Idx, x in enumerate(aCustom.split('\n')):
            Rule = x.strip()
            if (Rule):
                Lines.insert(IdxPos + 1 + Idx, Rule)
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
