#Created:     2024.04.03
#Author:      Vladimir Vons <VladVons@gmail.com>
#License:     GNU, see LICENSE for more details


__version__ = '1.0.60'
__date__ =  '2024.11.15'
__author__ = 'Vladimir Vons'
__email__ = 'VladVons@gmail.com'
__url__ = 'http://oster.com.ua'


def GetAppVer() -> dict:
    return {
        'app_name': 'vCrawler',
        'app_ver' : __version__,
        'app_date': __date__,
        'author':  f'{__author__ }, {__email__}',
        'home': __url__
    }
