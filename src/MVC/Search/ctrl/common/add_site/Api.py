# Created: 2024.12.22
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibCtrl as Lib
from ..._inc.email import SendMail


class TMain(Lib.TCtrlBase):
    async def Main(self, **aData):
        Subject = 'add site'
        Res = {
            'dbl_breadcrumbs': Lib.DblGetBreadcrumbs([[Subject, '']])
        }

        Post = aData.get('post')
        if (not Post):
            return Res

        Body = {
            'site': Post['site'],
            'phone': Post['phone'],
            'message': Post['message']
        }
        Ip = Lib.DeepGetByList(aData, ['session', 'ip'])
        R = await SendMail(self, Post['email'], Subject, Body, Ip)
        return Res | R
