#Created:     2024.04.03
#Author:      Vladimir Vons <VladVons@gmail.com>
#License:     GNU, see LICENSE for more details


import os
import sys
import platform
#
from Inc.Misc.Info import GetSysInfo, DictToText


__version__ = '1.0.1'
__date__ =  '2024.04.03'



def GetAppVer() -> dict:
    return {
        'app_name': 'vCrawler',
        'app_ver' : __version__,
        'app_date': __date__,
        'author':  'Vladimir Vons, VladVons@gmail.com',
        'home': 'http://oster.com.ua',
    }

def GetInfo() -> dict:
    Res = GetAppVer()
    Res.update(GetSysInfo())
    return Res

def GetInfoText():
    Data = GetInfo()
    return DictToText(Data)
