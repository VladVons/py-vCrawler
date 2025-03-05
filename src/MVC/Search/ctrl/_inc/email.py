# Created: 2025.03.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

import json
from Inc.Misc.Mail import TMail, TMailSend, TMailSmtp
import IncP.LibCtrl as Lib

async def SendMail(self, aEmail: str, aSubject: str, aBody: dict, aIp: str):
    Dbl = await self.ExecModelImport(
        'inbox',
        {
            'method': 'InsMail',
            'param': {
                'aMail': aEmail,
                'aSubject': aSubject,
                'aBody': json.dumps(aBody, indent=2, ensure_ascii=False),
                'aIp': aIp,
                'aInboxEn': 'in'
            }
        }
    )

    ConfSmtp = self.GetConf('mail_smtp')
    Smtp = TMailSmtp(**ConfSmtp)
    Data = TMailSend(
        mail_from = ConfSmtp['username'],
        mail_to = [aEmail] + self.GetConf('mail_admin'),
        mail_subject = f'{aSubject} findwares.com',
        mail_body = json.dumps(aBody, indent=2, ensure_ascii=False)
    )

    try:
        await TMail(Smtp).Send(Data)
        Msg = 'your request is sent'
    except Exception as E:
        Msg = 'error'
        Lib.Log.Print(1, 'x', 'TMail error', aE=E)

    return {
        'id': Dbl.Rec.id,
        'msg': Msg,
    }
