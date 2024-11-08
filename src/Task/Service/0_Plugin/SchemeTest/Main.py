# Created: 2024.10.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import sys
import json
from bs4 import BeautifulSoup

#
from Inc.Misc.PlayWrite import UrlGetData as UrlGetData_PW
from Inc.Misc.aiohttpClient import UrlGetData
from Inc.Scheme.Scheme import TScheme
from Inc.Var.Dict import DeepGetByList
from Inc.Var.Obj import GetTree
from IncP.Log import Log


class TSchemer():
    def __init__(self, aDir: str):
        self.Dir = aDir
        assert os.path.exists(self.Dir), f'Directory does not exist {self.Dir}'

    @staticmethod
    def CheckUrls(aUrls: list[str]) -> int:
        ErrCnt = 0
        for xUrl in aUrls:
            if (isinstance(xUrl, str)) and (not xUrl.startswith('http')):
                ErrCnt += 1
                Log.Print(1, 'i', f'Missed http {xUrl}')
        return ErrCnt

    @staticmethod
    def CheckFields(aPipe: dict, aFieldsNeed: list[str], aFields: list[str]) -> int:
        ErrCnt = 0

        Dif = set(aFieldsNeed) - set(aFields)
        if (Dif):
            ErrCnt += 1
            Log.Print(1, 'i', f'Missed {sorted(Dif)}')

        for xKey, xVal in aPipe.items():
            if (not xVal) and (not isinstance(xVal, bool)):
                Log.Print(1, 'i', f'Empty {xKey}')

        Val = aPipe.get('price')
        if (Val) and (not isinstance(Val[0], (int, float))):
            ErrCnt += 1
            Log.Print(1, 'i', f'`price` must be float {Val[0]}')

        return ErrCnt

    def ReadFile(self, aFile: str, aMode = 'r') -> str:
        File = self.Dir + '/' + aFile
        if (os.path.exists(File)):
            if (aMode == 'r'):
                with open(File, 'r', encoding='utf8') as hFile:
                    return hFile.read()
            else:
                with open(File, 'rb') as hFile:
                    return hFile.read()

    def WriteFile(self, aFile: str, aData: str):
        File = self.Dir + '/' + aFile
        if (isinstance(aData, str)):
            with open(File, 'w', encoding='utf8') as hFile:
                hFile.write(aData)
        else:
            with open(File, 'wb') as hFile:
                hFile.write(aData)

    def LoadScheme(self, aType: str) -> dict:
        Data = self.ReadFile(aType + '.json')
        if (Data):
            try:
                return json.loads(Data)
            except json.decoder.JSONDecodeError as E:
                File = self.Dir + '/' + aType + '.json'
                Log.Print(1, 'e', f'File: {File}. Err: {E}')
                sys.exit()

    @staticmethod
    def GetKeys(aScheme: dict) -> list:
        Res = []
        for _Nested, _Path, Obj, _Depth in GetTree(aScheme):
            if (isinstance(Obj, list)) and (len(Obj) > 0) and (Obj[0] == 'as_dict'):
                Res += Obj[1].keys()
        return sorted(set(Res))

    def TestHtml(self, aScheme: dict, aHtml: str, aType: str) -> dict:
        BSoup = BeautifulSoup(aHtml, 'lxml')
        #q1 = Soup.find('div', string='Замовити')
        #q1 = BSoup.find('div', class_='catalog_block items')

        #DeepSetByList(aScheme, [aType, 'info', 'url'], [Url])
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

        match aType:
            case 'product':
                KeysNeed = ['name', 'brand', 'image', 'images', 'stock', 'price', 'price_old', 'category', 'features', 'description']
                Urls = []
                if (isinstance(Pipe.get('images'), list)):
                    Urls += Pipe['images']
                if (isinstance(Pipe.get('image'), str)):
                    Urls += [Pipe['image']]
            case 'category':
                KeysNeed = ['href', 'name', 'stock', 'price', 'pager']
                Urls = []
                if (isinstance(Pipe.get('products'), list)):
                    Urls += [x.get('href') for x in Pipe['products']]
                if (isinstance(Pipe.get('pipe'), list)):
                    Urls += Pipe['pager']
            case _:
                raise ValueError(f'unknown type {aType}')

        #Keys = self.GetKeys(aScheme)
        Keys = list(Pipe.keys())

        Err |= bool(self.CheckFields(Pipe, KeysNeed, Keys))
        Err |= bool(self.CheckUrls(Urls))
        return {'err': Err , 'pipe': Pipe}

    async def Test(self, aType: str):
        Scheme = self.LoadScheme(aType)
        assert(Scheme), f'Err: No scheme loaded for {self.Dir}->{aType}'

        Cnt = 0
        Urls = DeepGetByList(Scheme, [aType, 'info', 'url'])
        if (not isinstance(Urls, list)):
            Data = DeepGetByList(Scheme, [aType, 'info', 'urls'])
            Urls = [xVal for xVal in Data.values()]

        for Idx, xUrl in enumerate(Urls):
            if (xUrl) and (not xUrl.startswith('-')):
                Log.Print(1, 'i', f'Test(). {xUrl}')

                Cnt += 1
                File = f'{aType}_{Idx+1}.html'
                Data = self.ReadFile(File, 'rb')
                if (not Data):
                    Reader = DeepGetByList(Scheme, [aType, 'info', 'reader'], '')
                    if (not Reader):
                        Reader = 'aiohttp'

                    Log.Print(1, 'i', f'Get url with {Reader}')
                    match Reader:
                        case 'playwright' | '':
                            DataU = await UrlGetData_PW(xUrl)
                        case 'aiohttp':
                            DataU = await UrlGetData(xUrl)
                        case _:
                            raise ValueError(f'Unknown reader {Reader}')

                    if (DataU['status'] != 200):
                        print(f'Error reading {xUrl}', DataU['status'], DataU['err'])
                        continue

                    Data = DataU['data']
                    self.WriteFile(File, Data)

                    BSoup = BeautifulSoup(Data, 'lxml')
                    DataP = BSoup.prettify()
                    File = f'{aType}_{Idx+1}_human.html'
                    self.WriteFile(File, DataP)

                Res = self.TestHtml(Scheme, Data, aType)
                #if (not Res['err']):
                if (not True):
                    Data = json.dumps(Res['pipe'], indent=2, ensure_ascii=False)
                    self.WriteFile(File + '.json', Data)
                    print('Ok. Saved', File + '.json')

        if (not Cnt):
            Log.Print(1, 'i', 'Err: No url parsed')
