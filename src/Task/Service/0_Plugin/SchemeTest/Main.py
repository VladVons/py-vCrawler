# Created: 2024.10.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import json
from bs4 import BeautifulSoup

#
from Inc.Misc.PlayWrite import UrlGetData as UrlGetData_PW
from Inc.Misc.aiohttpClient import UrlGetData
from Inc.Scheme.Scheme import TScheme
from Inc.Var.Dict import DeepGetByList
from Inc.Var.Obj import Iif
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
    def CheckFields(aPipe: dict, aFields: list[str]) -> int:
        ErrCnt = 0
        for xField in aFields:
            if (not xField.startswith('-')):
                Val = aPipe.get(xField)
                if (Val is None):
                    ErrCnt += 1
                    Log.Print(1, 'i', f'Missed {xField}')
                else:
                    if (xField == 'price'):
                        if (not isinstance(Val[0], (int, float))):
                            Log.Print(1, 'i', f'`price` must be float {Val[0]}')
                            ErrCnt += 1
        return ErrCnt

    def ReadFile(self, aFile: str) -> str:
        File = self.Dir + '/' + aFile
        if (os.path.exists(File)):
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

    async def Test(self, aType: str):
        Scheme = self.LoadScheme(aType)
        assert(Scheme), f'Err: No scheme loaded for {self.Dir}->{aType}'

        Cnt = 0
        Urls = DeepGetByList(Scheme, [aType, 'info', 'url'])
        for Idx, xUrl in enumerate(Urls):
            if (not xUrl.startswith('-')):
                Cnt += 1
                File = f'{aType}_{Idx+1}.html'
                Data = self.ReadFile(File)
                if (not Data):
                    Reader = DeepGetByList(Scheme, [aType, 'info', 'reader'], 'aiohttp')
                    Log.Print(1, 'i', f'Get url with {Reader}')
                    if (Reader == 'playwright'):
                        DataU = await UrlGetData_PW(xUrl)
                    elif (Reader == 'aiohttp'):
                        DataU = await UrlGetData(xUrl)
                    else:
                        raise ValueError(f'Unknown reader {Reader}')

                    if (DataU['status'] != 200):
                        print(f'Error reading {xUrl}')
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
