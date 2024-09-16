# Created: 2024.04.15
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import re
import gzip
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from protego import Protego
from playwright.async_api import async_playwright
#
from Inc.Misc.aiohttpClient import UrlGetData
from Inc.Util.Obj import GetTree, Iif
#from IncP.Log import Log


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

async def InitRobots(aUrl: str, aCustom: str = '') -> Protego:
    Parsed = urlparse(aUrl)
    Url = f'{Parsed.scheme}://{Parsed.hostname}/robots.txt'
    UrlData = await UrlGetData(Url)
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

    UrlData = await UrlGetData(aUrl)
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
