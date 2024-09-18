import os
import sys
import json
import asyncio
from bs4 import BeautifulSoup
#
from Inc.Misc.PlayWrite import UrlGetData as UrlGetData_PW
from Inc.Misc.aiohttpClient import UrlGetData
from Inc.Scheme.Scheme import TScheme, TSchemeExt, TSchemeApi
from Inc.Util.ModHelp import GetClass
from Inc.Util.Obj import Iif, IifNone, DeepGetByList, GetTree


DirRoot = 'sites/used/ua'

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
            Urls = IifNone(Pipe.get('images'), []) + [IifNone(Pipe.get('image'), [])]
        elif (aType == 'category'):
            Fields = ['products', 'pager']
            Products = IifNone(Pipe['products'], [])
            Urls = IifNone(Pipe.get('pager'), []) + [x['href'] for x in Products]
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

        Urls = DeepGetByList(Scheme, [aType, 'info', 'url'])
        for Idx, xUrl in enumerate(Urls):
            if (not xUrl.startswith('-')):
                File = f'{aType}_{Idx+1}.html'
                Data = self.ReadFile(File)
                if (not Data):
                    Reader = DeepGetByList(Scheme, [aType, 'info', 'reader'])
                    if (Reader == 'emulator'):
                        DataU = await UrlGetData_PW(xUrl)
                    else:
                        DataU = await UrlGetData(xUrl)

                    if (DataU['status'] == 200):
                        self.WriteFile(File, DataU['data'])
                    Data = DataU['data']

                Res = self.TestHtml(Scheme, Data, aType)
                #if (not Res['err']):
                if (True):
                    Data = json.dumps(Res['pipe'], indent=2, ensure_ascii=False)
                    self.WriteFile(File + '.json', Data)
                    print('Ok. Saved', File + '.json')


def GetAllMacroses() -> dict:
    Res = {}
    for xDir in os.listdir(DirRoot):
        Dir = os.path.join(DirRoot, xDir)
        if os.path.isdir(Dir):
            for xFile in ['product', 'category']:
                Schemer = TSchemer(xDir)
                Scheme = Schemer.LoadScheme(xFile)
                if (Scheme):
                    Macroses = Schemer.GetMacroses(Scheme)
                    for Key, Val in Macroses.items():
                        Res[Key] = Res.get(Key, 0) + Val
    PopularFirst = sorted(Res.items(), key=lambda item: item[1], reverse=True)
    return dict(PopularFirst)

async def Main():
    os.system('clear')
    print(os.getcwd())
    print(sys.version)
    #
    # Macroses = GetAllMacroses()
    # for Idx, (Key, Val) in enumerate(Macroses.items()):
    #     print(f'{Idx+1:3} {Key:15} {Val:3}')
    #
    #
    await TSchemer('mt.org.ua').Test('product')
    #await TSchemer('setka.ua').Test('category')
    #
    print("done")

asyncio.run(Main())
