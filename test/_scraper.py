import os
import sys
import json
import glob
from bs4 import BeautifulSoup
#
from Inc.Scheme.Scheme import TScheme, TSoupScheme, TSchemeExt


class TSchemer():
    def __init__(self, aSite: str):
        self.Dir = f'sites/{aSite}'

    @staticmethod
    def CheckFields(aFields: list[str], aData: dict):
        for xField in aFields:
            if (not xField.startswith('-')):
                Val = aData.get(xField)
                if (Val is None):
                    print('Missed', xField)
                else:
                    if (xField == 'price'):
                        if (not isinstance(Val[0], (int, float))):
                            print('price must be float')

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
        #q1 = Soup.find('span', string='Замовити')
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
        Fields = {
            'product': ['name', 'brand', 'image', 'images', 'stock', 'price', 'price_old', 'category', '-sku', '-mpn', 'features', 'description'],
            'category': ['products']
        }
        self.CheckFields(Fields[aType], Pipe)

        File = aFile + '.json'
        if os.path.exists(File):
            os.remove(File)
        if (not Err) and (not Scheme.Err):
            Data = json.dumps(Pipe, indent=2, ensure_ascii=False)
            self.WriteFile(File, Data)
            print('Saved', File)

    def Test(self, aType: str):
        Html = self.FindHtml(aType)
        for xFile in Html:
            self.TestHtml(xFile, aType)

os.system('clear')
print(os.getcwd())
print(sys.version)
#
#TSchemer('acomp.com.ua').Test('product')
#TSchemer('as-it.ua').Test('product')
#TSchemer('cibermag.com').Test('product')
#TSchemer('h-store.in.ua').Test('product')
#TSchemer('laptop-planet.com.ua').Test('product')
#TSchemer('laptopchik.top').Test('product')
#TSchemer('lapstore.com.ua').Test('product')
#TSchemer('lux-pc.com').Test('product')
TSchemer('pc.com.ua').Test('product')
#TSchemer('setka.ua').Test('product')
#
print("done")
