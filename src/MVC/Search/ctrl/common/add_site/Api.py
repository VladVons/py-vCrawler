# Created: 2024.12.22
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import json
#
from Inc.Misc.Mail import TMail, TMailSend, TMailSmtp
import IncP.LibCtrl as Lib


class TMain(Lib.TCtrlBase):
    async def Main(self, **aData):
        aLangId, CountryId = Lib.GetDictDefs(
            aData.get('query'),
            ('lang_id', 'country_id'),
            (1, 1)
        )

        Res = {
            'dbl_breadcrumbs': Lib.DblGetBreadcrumbs([['add site', '']])
        }

        Post = aData.get('post')
        if (not Post):
            return Res

        Body = {
            'country_id': CountryId,
            'site': Post['site'],
            'phone': Post['phone'],
            'category': Post['category']
        }

        Subject = 'add site to catalog'
        Dbl = await self.ExecModelImport(
            'inbox',
            {
                'method': 'InsMail',
                'param': {
                    'aMail': Post['email'],
                    'aSubject': Subject,
                    'aBody': json.dumps(Body, indent=2, ensure_ascii=False),
                    'aIp': Lib.DeepGetByList(aData, ['session', 'ip']),
                    'aInboxEn': 'in'
                }
            }
        )

        Arr = Lib.ResLang(aData, 'body', ['no value'])
        Body['message'] = '\n'.join(Arr)

        ConfSmtp = self.GetConf('mail_smtp')
        Smtp = TMailSmtp(**ConfSmtp)
        Data = TMailSend(
            mail_from = ConfSmtp['username'],
            mail_to = [Post['email']] + self.GetConf('mail_admin'),
            mail_subject = f'{Subject} findwares.com',
            mail_body = json.dumps(Body, indent=2, ensure_ascii=False)
        )

        try:
            await TMail(Smtp).Send(Data)
            Msg = 'your request is sent'
        except Exception as E:
            Msg = 'error'
            Lib.Log.Print(1, 'x', 'TMail error', aE=E)

        ResExt = {
            'id': Dbl.Rec.id,
            'msg': Msg,
        }
        return Res | ResExt
