import time
import asyncio
import aiohttp
from Inc.ParserSpec.TestAll import TSpecComp
from Inc.VFS.Disk import TFsDisk
from Inc.VFS.Mem import TFsMem
from Inc.Misc.aiohttpClient import DownloadChunksToFile

def Test1():
    TimeAt = time.time()
    File = 'Temp/cpu-intel.txt'
    #File = 'Temp/usedpc-1000.txt'
    SpecComp = TSpecComp()
    SpecComp.ParseFile(File)
    print(round(time.time() - TimeAt, 2), 'sec')

async def Test2():
    Dir = 'dir1/dir2'
    File = f'{Dir}/test1.txt'

    #Fs = TFsDisk('./')
    Fs = TFsMem()

    File1 = f'vCrawler.log'
    q1 = Fs.FileWrite(File1, '12345678901234567890'.encode())
    async for xBlock, _xSize in Fs.FileReadChunk(File1, 5):
        print(xBlock)

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

    url = 'https://d12.drivemusic.club/dl/4KGkN0NL-t2PVFVnh9lAfw/1734329489/download_music/2012/10/detskie-luch-solnca-zolotogo.mp3'
    output_path = 'luch-solnca-zolotogo.mp3'

    #await DownloadChunksToFile(url, output_path)

    Fs = TFsDisk('./')

    BlockSize = 65536
    async with aiohttp.ClientSession() as Session:
        async with Session.get(url) as Response:
            if (Response.status == 200):
                await Fs.FileWriteChunk(output_path, Response.content, BlockSize)
    print('done')

async def Main():
    #Test1()
    #await Test2()
    await Test3()

asyncio.run(Main())
