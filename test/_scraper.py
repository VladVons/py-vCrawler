import os
import sys
import json
import asyncio
import aiohttp
from bs4 import BeautifulSoup
#
from Inc.Misc.PlayWrite import GetUrlData as GetUrlData_PW
from Inc.Scheme.Scheme import TScheme, TSchemeExt, TSchemeApi
from Inc.Util.ModHelp import GetClass
from Inc.Util.Obj import Iif, IifNone, DeepGetByList, GetTree


DirRoot = 'sites/used'

class TSchemer():
    def __init__(self, aSite: str):
        self.Dir = f'{DirRoot}/{aSite}'
        assert os.path.exists(self.Dir), f'Directory does not exist {self.Dir}'

    @staticmethod
    def CheckUrls(aUrls: list[str]) -> int:
        ErrCnt = 0
        for xUrl in aUrls:
            if (not xUrl.startswith('http')):
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

    @staticmethod
    async def GetUrlData(aUrl: str) -> object:
        Headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
            'Accept-Language': 'uk'
        }

        async with aiohttp.ClientSession(headers=Headers, max_field_size=16384) as Session:
            try:
                async with Session.get(aUrl, allow_redirects=True) as Response:
                    Data = await Response.read()
                    Res = {'data': Data, 'status': Response.status}
            except Exception as E:
                Res = {'err': str(E), 'status': -1}
        return Res

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
            Urls = IifNone(Pipe['images'], []) + [IifNone(Pipe['image'], [])]
        elif (aType == 'category'):
            Fields = ['products', 'pager']
            Products = IifNone(Pipe['products'], [])
            Urls = IifNone(Pipe['pager'], []) + [x['href'] for x in Products]
        Err |= bool(self.CheckFields(Pipe, Fields))
        Err |= bool(self.CheckUrls(Urls))
        return {'err': Err , 'pipe': Pipe}

    @staticmethod
    def GetMacroses(aScheme: dict) -> list:
        Res = []
        BS4 = ['find', 'find_all', 'text', 'get']
        Methods = GetClass(TSchemeApi) + GetClass(TSchemeExt)
        Methods = [xMethod[0] for xMethod in Methods] + BS4
        for _Nested, _Path, Obj, _Depth in GetTree(aScheme):
            if (isinstance(Obj, list)) and (len(Obj) > 0):
                Method = Obj[0]
                if (isinstance(Method, str)) and (Method in Methods):
                    Res.append(Method)
        return sorted(set(Res))

    async def Test(self, aType: str):
        Scheme = self.LoadScheme(aType)

        Urls = DeepGetByList(Scheme, [aType, 'info', 'url'])
        for Idx, xUrl in enumerate(Urls):
            if (not xUrl.startswith('-')):
                File = f'{aType}_{Idx+1}.html'
                Data = self.ReadFile(File)
                if (not Data):
                    Reader = DeepGetByList(Scheme, [aType, 'info', 'reader'])
                    if (Reader == 'emulator'):
                        DataU = await GetUrlData_PW(xUrl)
                    else:
                        DataU = await self.GetUrlData(xUrl)

                    if (DataU['status'] == 200):
                        self.WriteFile(File, DataU['data'])
                    Data = DataU['data']

                Res = self.TestHtml(Scheme, Data, aType)
                if (not Res['err']):
                    Data = json.dumps(Res['pipe'], indent=2, ensure_ascii=False)
                    self.WriteFile(File + '.json', Data)
                    print('Ok. Saved', File + '.json')


def GetAllMacroses() -> list:
    Res = []
    for xDir in os.listdir(DirRoot):
        Dir = os.path.join(DirRoot, xDir)
        if os.path.isdir(Dir):
            for xFile in ['product', 'category']:
                Schemer = TSchemer(xDir)
                Scheme = Schemer.LoadScheme(xFile)
                if (Scheme):
                    Macroses = Schemer.GetMacroses(Scheme)
                    Res += Macroses
    return sorted(set(Res))

async def Main():
    os.system('clear')
    print(os.getcwd())
    print(sys.version)
    #
    Macroses = GetAllMacroses()
    for xMacros in Macroses:
        print(xMacros)
    #
    #await TSchemer('1x1.com.ua').Test('product')
    #await TSchemer('1x1.com.ua').Test('category')
    #
    #await TSchemer('acomp.com.ua').Test('product')
    #await TSchemer('acomp.com.ua').Test('category')
    #
    #await TSchemer('as-it.ua').Test('product')
    #await TSchemer('as-it.ua').Test('category')
    #
    #await TSchemer('cibermag.com').Test('product')
    #
    #await TSchemer('europc.ua').Test('product')
    #await TSchemer('europc.ua').Test('category')
    #
    #await TSchemer('gazik.ua').Test('product')
    #await TSchemer('gazik.ua').Test('category')
    #
    #await TSchemer('h-store.in.ua').Test('product')
    #await TSchemer('laptop-planet.com.ua').Test('product')
    #await TSchemer('laptopchik.top').Test('product')
    #
    #await TSchemer('lapstore.com.ua').Test('product')
    #await TSchemer('lapstore.com.ua').Test('category')
    #
    #await TSchemer('lux-pc.com').Test('product')
    #await TSchemer('lux-pc.com').Test('category')
    #
    #await TSchemer('pc.com.ua').Test('product')
    #await TSchemer('pc.com.ua').Test('category')
    #
    #await TSchemer('setka.ua').Test('product')
    #await TSchemer('setka.ua').Test('category')
    #
    print("done")

asyncio.run(Main())

