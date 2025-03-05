# Created: 2025.03.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibCtrl as Lib
from ..._inc.email import SendMail

class TMain(Lib.TCtrlBase):
    async def Main(self, **aData):
        Subject = 'contact us'
        Res = {
            'dbl_breadcrumbs': Lib.DblGetBreadcrumbs([[Subject, '']])
        }

        Post = aData.get('post')
        if (not Post):
            return Res

        Body = {
            'subject': Post['subject'],
            'message': Post['message']
        }
        Ip = Lib.DeepGetByList(aData, ['session', 'ip'])
        R = await SendMail(self, Post['email'], f'{Subject}. {Post['subject']}', Body, Ip)
        return Res | R
