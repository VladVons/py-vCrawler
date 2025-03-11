# Created: 2025.03.11
# Author: Vladimir Vons <VladVons@gmail.com>

import asyncio
#
from Inc.Misc.SmsGW import TSmsGW
from Inc.DbList import TDbList

Connect = {
    'aUrl': 'http://192.168.2.208:8080',
    'aUser': 'sms',
    'aPassw': 'F63VRxdn'
}

FmtText = '''
{Name},
В Україні створено каталог вживаних комп’ютерів.
Тут ви знайдете найкращі пропозиції.
https://it.findwares.com/uk
'''

# FmtText = '''
# {Name},
# Повний каталог бу комп’ютерів.
# https://it.findwares.com'''

# FmtText = '''
# {Name},
# Для Вас каталог вживаних комп’ютерів.
# https://it.findwares.com'''


async def Main1():
    Connect = {
        'aUrl': 'http://192.168.2.208:8080',
        'aUser': 'sms',
        'aPassw': 'F63VRxdn'
    }
    SmsGW = TSmsGW(**Connect)

    Dbl = TDbList(
        ['phone', 'name'],
        [
            ['-+380974274859', 'Ольга'],
            ['+380635107383', 'Віктор'],
            ['-+380976646510', 'Володимир'],
            ['-+380677697216', 'Богдан'],
        ]
    )

    for Rec in Dbl:
        Text = FmtText.format(Name=Rec.name)
        Phone = Rec.phone
        if (not Rec.phone.startswith('-')):
            Res= await SmsGW.Send([Phone], Text)
            print(f'Phone: {Phone}, Status: {Res["status"]}, Data: {Res["data"]}')
            await asyncio.sleep(1)

async def Main2():
    SmsGW = TSmsGW(**Connect)

    # Text = FmtText.format(Name='Володимир')
    # Phones = ['0976646510']
    # await SmsGW.Send(Phone, Text)

    #Res = await SmsGW.Status('KeYuIsLPEq7sLl-5ro1BF')
    #Res = await SmsGW.Logs()
    Res = await SmsGW.Health()
    print(f'Status: {Res["status"]}, Data: {Res["data"]}')


asyncio.run(Main2())
