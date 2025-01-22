import time
import asyncio
import aiohttp
from Inc.ParserSpec.LibsComp import TLibsComp
from Inc.VFS.Disk import TFsDisk
from Inc.VFS.Mem import TFsMem
from Inc.Misc.aiohttpClient import DownloadChunksToFile


def Stair(aWord: str, aCountFrom: int, aCountTo: int):
    for i in range(aCountFrom, aCountTo):
        Count = abs(i)
        print(Count, aWord * Count)

def Test1():
    TimeAt = time.time()
    File = 'Temp/cpu-intel.txt'
    #File = 'Temp/usedpc-1000.txt'
    LibsComp = TLibsComp()
    LibsComp.ParseFile(File)
    print(round(time.time() - TimeAt, 2), 'sec')

async def Test2():
    Dir = 'dir1/dir2'
    File = f'{Dir}/test1.txt'

    #Fs = TFsDisk('./')
    Fs = TFsMem()

    Fs.FileDelete(File)
    Fs.DirCreate(Dir)
    q1 = Fs.FileWrite(File, '12345678901234567890'.encode())
    q2 = Fs.FileSize(File)
    q3 = Fs.FileRead(File).decode()
    Fs.FileDelete(File)
    pass

async def Test3():
    url = "https://mp4-download.com/4k-MP4"
    output_path = "4k.mp4"

    url = "https://link.testfile.org/15MB"
    output_path = "15mb.dat"

    url = 'https://mp3uk.net/mp3/files/niletto-luch-solnca-zolotogo-mp3.mp3'
    output_path = 'luch-solnca-zolotogo.mp3'

    #await DownloadChunksToFile(url, output_path)

    Fs = TFsDisk('./temp/123')

    BlockSize = 65536
    async with aiohttp.ClientSession() as Session:
        async with Session.get(url) as Response:
            if (Response.status == 200):
                #await Fs.FileWriteChunk(output_path, Response.content, BlockSize)
                await Fs.FileWriteChunkPos(output_path, Response.content, BlockSize, 0, Response.content_length)

    print('done')

async def Main():
    Stair('*', -5, 6)
    #Test1()
    #await Test2()
    #await Test3()
    pass

asyncio.run(Main())

