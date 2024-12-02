from Inc.ParserSpec import TSpecCpu, TSpecRam, TSpecStorage, TSpecOs, TSpecScreen


def Test_01():
    SpecObj = {
        '-cpu': TSpecCpu(),
        '-ram': TSpecRam(),
        '-disk': TSpecStorage(),
        'screen': TSpecScreen(),
        '-os': TSpecOs()
    }

    File = 'Inc/ParserSpec/test/Processor-intel.txt'
    with open(File, 'r', encoding='utf8') as F:
        Lines = F.readlines()

    for xLine in Lines:
        xLine = xLine.strip()
        if (not xLine) or (xLine.startswith('-')):
            continue

        print(xLine)
        for xKey, xVal in SpecObj.items():
            if (not xKey.startswith('-')):
                R = xVal.Parse(xLine)
                if (R):
                    print(R)
        print()

Test_01()
