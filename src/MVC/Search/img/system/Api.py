# Created: 2023.03.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.VFS.Disk import TFsDisk
from Task.Search.SrvImg.Api import TApiImg
import IncP.LibImg as Lib


class TMain(Lib.TImgBase):
    def __init__(self, aApiImg: TApiImg):
        super().__init__(aApiImg)
        self.Fs = TFsDisk(self.Conf.dir_root)

    async def GetFiles(self, aFiles: list[str]) -> dict:
        Calls = ['Exists'] + [[xFile] for xFile in aFiles]
        Exists = self.Fs.MassCall(Calls)

        Res = [
            self.Conf.url + '/' + Lib.Iif(xExists, xFile, self.Conf.no_image)
            for xExists, xFile in zip(Exists, aFiles)
        ]
        return Res
