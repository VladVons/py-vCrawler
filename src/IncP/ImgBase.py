# Created: 2023.04.18
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Task.Search.SrvImg.Api import TApiImg


class TImgBase():
    def __init__(self, aApiImg: TApiImg):
        self.ApiImg = aApiImg

    @property
    def Conf(self):
        return self.ApiImg.Conf
