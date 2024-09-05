import os
import sys
import json
import glob
from bs4 import BeautifulSoup
#
from Inc.Util.Obj import IifNone
from Inc.Scheme.Scheme import TScheme, TSoupScheme, TSchemeExt


class TSchemer():
    def __init__(self, aSite: str):
        self.Dir = f'sites/used/{aSite}'
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

    def ReadFile(self, aFile: str) -> str:
        with open(self.Dir + '/' + aFile, 'r', encoding='utf8') as hFile:
            return hFile.read()

    def WriteFile(self, aFile: str, aData: str):
        with open(self.Dir + '/' + aFile, 'w', encoding='utf8') as hFile:
            hFile.write(aData)

    def FindHtml(self, aType: str) -> list[str]:
        Pattern = f'{self.Dir}/{aType}*.html'
        Files = glob.glob(Pattern)
        return sorted([os.path.basename(xFile) for xFile in Files])

    def TestHtml(self, aFile, aType: str):
        Data = self.ReadFile(aType + '.json')
        Scheme = json.loads(Data)

        Data = self.ReadFile(aFile)
        BSoup = BeautifulSoup(Data, 'lxml')
        #q1 = Soup.find('div', string='Замовити')
        #q1 = BSoup.find('div', class_='catalog_block items')
        Scheme = TScheme(Scheme)
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

        File = aFile + '.json'
        if os.path.exists(File):
            os.remove(File)
        if (not Err) and (not Scheme.Err):
            Data = json.dumps(Pipe, indent=2, ensure_ascii=False)
            self.WriteFile(File, Data)
            print('Saved', File)

    def Test(self, aType: str):
        Html = self.FindHtml(aType)
        assert(Html), f'No {aType} html found'

        for xFile in Html:
            self.TestHtml(xFile, aType)

os.system('clear')
print(os.getcwd())
print(sys.version)
#
#TSchemer('acomp.com.ua').Test('product')
#TSchemer('acomp.com.ua').Test('category')
#
#TSchemer('as-it.ua').Test('product')
#TSchemer('as-it.ua').Test('category')
#
#TSchemer('cibermag.com').Test('product')
#TSchemer('h-store.in.ua').Test('product')
#TSchemer('laptop-planet.com.ua').Test('product')
#TSchemer('laptopchik.top').Test('product')
#TSchemer('lapstore.com.ua').Test('product')
#TSchemer('lux-pc.com').Test('product')
#
TSchemer('pc.com.ua').Test('product')
#TSchemer('pc.com.ua').Test('category')
#
#TSchemer('setka.ua').Test('product')
#TSchemer('setka.ua').Test('category')
#
print("done")
