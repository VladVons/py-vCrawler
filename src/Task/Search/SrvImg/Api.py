# Created: 2023.03.02
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.DataClass import DDataClass
from IncP.ApiBase import TApiBase
from IncP.Plugins import TImgs


@DDataClass
class TExec():
    Method: object
    Module: object


@DDataClass
class TApiImgConf():
    url: str = 'http://localhost:8183/img'
    dir_route: str = 'MVC/                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      /img'
    dir_root: str = 'Data/img'
    dir_thumb: str = 'thumb'
    no_image: str= 'no-product.png'
    size_thumb: int = 200
    size_product: int = 1024

class TApiImg(TApiBase):
    def __init__(self):
        super().__init__()

        Conf = self.GetConf()
        self.Conf = TApiImgConf(**Conf)

        self.Plugin = TImgs(Conf['dir_route'], self)

ApiImg = TApiImg()
