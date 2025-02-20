import os
import sys
import json
import time
import asyncio
from bs4 import BeautifulSoup
#
from Inc.Misc.PlayWrite import UrlGetData as UrlGetData_PW
from Inc.Misc.aiohttpClient import UrlGetData
from Inc.Scheme.Scheme import TScheme, TSchemeExt, TSchemeApi
from Inc.Util.ModHelp import GetClass
from Inc.Var.Obj import Iif, GetTree
from Inc.Var.Dict import DeepGetByList


DirRoot = 'sites/used/ua'


#https://googlechromelabs.github.io/chrome-for-testing/#stable
#from pyppeteer import launch, executablePath
#q1 = executablePath()
async def UrlGetData_pyppeteer(aUrl):
    #browser = await launch(headless=True, executablePath='./chromedriver')
    browser = await launch(headless=True)

    page = await browser.newPage()
    response = await page.goto(aUrl, waitUntil='domcontentloaded', timeout=10000)
    content = await page.content()
    await browser.close()

    return {
        'data': content,
        'status': response.status
    }

async def UrlGetData_httpx(aUrl: str):
    async with httpx.AsyncClient() as Client:
        try:
            Response = await Client.get(aUrl)
            Data = Response.html.render()
            Res = {'data': Response.content, 'status': Response.status_code}
        except Exception as E:
            Res = {'err': str(E), 'status': -1}
        return Res


class TSchemer():
    def __init__(self, aSite: str):
        self.Dir = f'{DirRoot}/{aSite}'
        assert os.path.exists(self.Dir), f'Directory does not exist {self.Dir}'

    @staticmethod
    def CheckUrls(aUrls: list[str]) -> int:
        ErrCnt = 0
        for xUrl in aUrls:
            if (isinstance(xUrl, str)) and (not xUrl.startswith('http')):
                ErrCnt += 1
                print('Missed http', xUrl)
        return ErrCnt

    @staticmethod
    def CheckFields(aPipe: dict, aFields: list[str]) -> int:
        ErrCnt = 0
        for xField in aFields:
            if (not xField.startswith('-')):
                Val = aPipe.get(xField)
                if (Val is None):
                    ErrCnt += 1
                    print('Missed', xField)
                else:
                    if (xField == 'price'):
                        if (not isinstance(Val[0], (int, float))):
                            print('price must be float')
                            ErrCnt += 1
        return ErrCnt

    def ReadFile(self, aFile: str) -> str:
        File = self.Dir + '/' + aFile
        if os.path.exists(File):
            with open(File, 'r', encoding='utf8') as hFile:
                return hFile.read()

    def WriteFile(self, aFile: str, aData: str):
        File = self.Dir + '/' + aFile
        Mode = Iif(isinstance(aData, str), 'w', 'wb')
        with open(File, Mode) as hFile:
            hFile.write(aData)

    def LoadScheme(self, aType: str) -> dict:
        Data = self.ReadFile(aType + '.json')
        if (Data):
            return json.loads(Data)

    def TestHtml(self, aScheme: dict, aHtml: str, aType: str) -> dict:
        BSoup = BeautifulSoup(aHtml, 'lxml')
        #q1 = Soup.find('div', string='Замовити')
        #q1 = BSoup.find('div', class_='catalog_block items')
        Scheme = TScheme(aScheme)
        Scheme.Parse(BSoup)
        Pipe = Scheme.GetPipe(aType)

        print()
        Err = False
        try:
            HumanJson = json.dumps(Pipe, indent=2, ensure_ascii=False)
            print(HumanJson)
        except Exception as _E:
            Err = True
            print(Pipe)

        print()
        for x in Scheme.Err:
            print(x)

        print()
        if (aType == 'product'):
            Fields = ['name', 'brand', 'image', 'images', 'stock', 'price', 'price_old', 'category', '-sku', '-mpn', 'features', 'description']
            Urls = []
            if (isinstance(Pipe.get('images'), list)):
                Urls += Pipe['images']
            if (isinstance(Pipe.get('image'), str)):
                Urls += [Pipe['image']]
        elif (aType == 'category'):
            Fields = ['products', 'pager']
            Urls = []
            if (isinstance(Pipe.get('products'), list)):
                Urls += [x.get('href') for x in Pipe['products']]
            if (isinstance(Pipe.get('pipe'), list)):
                Urls += Pipe['pager']
        Err |= bool(self.CheckFields(Pipe, Fields))
        Err |= bool(self.CheckUrls(Urls))
        return {'err': Err , 'pipe': Pipe}

    @staticmethod
    def GetMacroses(aScheme: dict) -> dict:
        Res = {}
        BS4 = ['find', 'find_all', 'text', 'get']
        Methods = GetClass(TSchemeApi) + GetClass(TSchemeExt)
        Methods = [xMethod[0] for xMethod in Methods] + BS4
        for _Nested, _Path, Obj, _Depth in GetTree(aScheme):
            if (isinstance(Obj, list)) and (len(Obj) > 0):
                Method = Obj[0]
                if (isinstance(Method, str)) and (Method in Methods):
                    if (Method not in Res):
                        Res[Method] = 0
                    Res[Method] += 1
        return Res

    async def Test(self, aType: str):
        Scheme = self.LoadScheme(aType)

        Cnt = 0
        Urls = DeepGetByList(Scheme, [aType, 'info', 'url'])
        for Idx, xUrl in enumerate(Urls):
            if (not xUrl.startswith('-')):
                Cnt += 1
                File = f'{aType}_{Idx+1}.html'
                Data = self.ReadFile(File)
                if (not Data):
                    Reader = DeepGetByList(Scheme, [aType, 'info', 'reader'], 'aiohttp')
                    print(f'read with {Reader}')
                    if (Reader == 'playwright'):
                        DataU = await UrlGetData_PW(xUrl)
                    elif (Reader == 'httpx'):
                        DataU = await UrlGetData_httpx(xUrl)
                    elif (Reader == 'pyppeteer'):
                        DataU = await UrlGetData_pyppeteer(xUrl)
                    else:
                        DataU = await UrlGetData(xUrl)

                    if (DataU['status'] != 200):
                        print(f'Error reading {xUrl}')
                        continue

                    self.WriteFile(File, DataU['data'])
                    Data = DataU['data']

                Res = self.TestHtml(Scheme, Data, aType)
                #if (not Res['err']):
                if (not True):
                    Data = json.dumps(Res['pipe'], indent=2, ensure_ascii=False)
                    self.WriteFile(File + '.json', Data)
                    print('Ok. Saved', File + '.json')

        if (not Cnt):
            print('Err: No url parsed')

def _GetFiles() -> list:
    Res = []
    for xDir in os.listdir(DirRoot):
        Dir = os.path.join(DirRoot, xDir)
        if os.path.isdir(Dir):
            for xFile in ['product', 'category']:
                if (os.path.exists(os.path.join(Dir, xFile + '.json'))):
                    Res.append((xDir, xFile))
    return Res

def GetAllMacroses() -> dict:
    Res = {}
    for xDir, xFile in _GetFiles():
        Schemer = TSchemer(xDir)
        Scheme = Schemer.LoadScheme(xFile)
        if (Scheme):
            Macroses = Schemer.GetMacroses(Scheme)
            for Key, Val in Macroses.items():
                Res[Key] = Res.get(Key, 0) + Val
    PopularFirst = sorted(Res.items(), key=lambda item: item[1], reverse=True)
    return dict(PopularFirst)

async def ParseAll() -> dict:
    for xDir, xFile in sorted(_GetFiles()):
        print(xDir, xFile)
        await TSchemer(xDir).Test(xFile)
        input('press enter...')

async def SpeedTest(aUrl: str):
    StartAt = time.time()
    for x in range(5):
        print('try', x+1)
        await UrlGetData_pyppeteer(aUrl)
        #await UrlGetData_PW(aUrl)
    print('time', time.time() - StartAt)

async def Main():
    os.system('clear')
    print(os.getcwd())
    print(sys.version)
    #
    #Macroses = GetAllMacroses()
    # for Idx, (Key, Val) in enumerate(Macroses.items()):
    #     print(f'{Idx+1:3} {Key:15} {Val:3}')
    #
    #await ParseAll()
    #await SpeedTest('https://setka.ua/c/noutbuki/noutbuki_1/page-4/')
    #
    #Url = 'https://recorder.com.ua/Igrovoy-sistemniy-blok-AMD-Ryzen-5-4500-32-GB-RAM-128-GB-SSD-500-GB-HDD-NV-Sistemnie-bloki-BU-609803_2'
    #Url = 'https://recorder.com.ua'
    #Url = 'https://setka.ua/c/noutbuki/noutbuki_1/'
    #Url = 'https://1x1.com.ua/product/dell_optiplex_3020_mt_i5-4590_4gb_500gb_hdd_t1'
    #q1 = await UrlGetData_PW(Url)


    #await TSchemer('trium.com.ua').Test('product')
    #await TSchemer('lviv.skladova.com.ua').Test('category')
    #await TSchemer('olx_shop.ua').Test('category')
    #await TSchemer('recorder.com.ua').Test('product')
    await TSchemer('pc.com.ua').Test('product')
    #
    print("done")

asyncio.run(Main())
