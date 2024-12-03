from Inc.ParserSpec import TSpecCpu, TSpecRam, TSpecStorage, TSpecOs, TSpecScreen, TSpecFormFactor


def Test_01():
    SpecObj = {
        '-cpu': TSpecCpu(),
        '-ram': TSpecRam(),
        '-disk': TSpecStorage(),
        'screen': TSpecScreen(),
        '-os': TSpecOs(),
        '-form': TSpecFormFactor()
    }

    File = 'Inc/ParserSpec/test/cpu-amd.txt'
    with open(File, 'r', encoding='utf8') as F:
        Lines = []
        for xLine in F.readlines():
            xLine = xLine.strip()
            if (xLine) and (not xLine.startswith('-')):
                Lines.append(xLine)

    for Idx, xLine in enumerate(Lines):
        print(f'{Idx+1}/{len(Lines)}: {xLine}')
        for xKey, xVal in SpecObj.items():
            if (not xKey.startswith('-')):
                R = xVal.Parse(xLine)
                if (R):
                    print(xKey, R)
        print()

Test_01()
