import time
from Inc.ParserSpec.TestAll import TSpecComp


TimeAt = time.time()
File = 'Temp/cpu-intel.txt'
#File = 'Temp/usedpc-1000.txt'
SpecComp = TSpecComp()
SpecComp.ParseFile(File)
print(round(time.time() - TimeAt, 2), 'sec')
