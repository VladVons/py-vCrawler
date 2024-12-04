import time
from Inc.ParserSpec.TestAll import TestAll


TimeAt = time.time()
File = 'Temp/cpu-intel.txt'
#File = 'Temp/usedpc-1000.txt'
TestAll(File)
print(round(time.time() - TimeAt, 2))