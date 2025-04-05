import time
import asyncio
import aiohttp
import requests
import ssl
from Inc.ParserSpec.LibsComp import TLibsComp
from Inc.VFS.Disk import TFsDisk
from Inc.VFS.Mem import TFsMem
from Inc.Misc.aiohttpClient import DownloadChunksToFile
from Inc.Var.Str import DecryptXor, EncryptXor

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

async def Download():
    #url = "https://recorder.com.ua/image/cache/catalog/oc_6341202044408332b85dfe909d05a8fbc4f425-592x343.jpg"
    #url = "https://midis.zp.ua/img/good/116364"
    #url = "https://nosta.com.ua/image/cache/catalog/nosta/PC%20%D0%BA%D1%83%D0%BF%D0%B8%D1%82%D1%8C/lenovo-tiny-desktop-thinkcentre-m73-front-18-700x500.png"
    url = "https://setka.ua/upload/resize_cache/iblock/ccf/450_450_140cd750bba9870f18aada2478b24840a/ldmhqjbyl31z90n0nh4xod404bwqlslr.jpg"

    filename = "downloaded_image.jpg"
    headers = {
        'User-Agent': 'python-requests/2.32.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': '*/*',
        'Connection': 'keep-alive'
    }

    # method 1 - status 200
    # response = requests.get(url)
    # headers = response.request.headers
    # if response.status_code == 200:
    #     with open(filename, "wb") as file:
    #             file.write(response.content)

    # session = requests.Session()
    # response = session.get(url)
    # headers = response.request.headers
    # cookies = session.cookies.get_dict()

    ssl_context = ssl.create_default_context()
    #ssl_context.set_ciphers("DEFAULT@SECLEVEL=1")  # Зниження рівня безпеки TLS
    ssl_context.check_hostname = False
    #ssl_context.verify_mode = ssl.CERT_NONE
    # ssl_context.options |= ssl.OP_NO_TLSv1_1
    # ssl_context.options |= ssl.OP_NO_TLSv1_2
    # ssl_context.options |= ssl.OP_NO_TLSv1_3
    ssl_context.options = 0

    #print(ssl_context.options)

    # method 2 - status 403
    async with aiohttp.ClientSession(headers=headers) as Session:
        async with Session.get(url, allow_redirects=True, ssl=ssl_context) as Response:
            if (Response.status == 200):
                Data = await Response.read()
                with open(filename, "wb") as file:
                    file.write(Data)
    pass



async def Main():
    #Stair('*', -5, 6)
    #Test1()
    #await Test2()
    #await Test3()
    await Download()
    pass

asyncio.run(Main())