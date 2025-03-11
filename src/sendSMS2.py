import re
import asyncio
import aiohttp
#
from Inc.DbList import TDbList

FmtText = '''
{Name},
В Україні запрацював каталог вживаних комп’ютерів-FindWares.
Тут знайдете найкращі пропозиції.
https://it.findwares.com
'''

# FmtText = '''
# {Name},
# В Україні запрацював каталог вживаних комп’ютерів-FindWares.
# Тут знайдете найкращі пропозиції.
# https://it.findwares.com'''

# FmtText = '''
# {Name},
# Повний каталог бу комп’ютерів.
# https://it.findwares.com'''

# FmtText = '''
# {Name},
# Для Вас каталог вживаних комп’ютерів.
# https://it.findwares.com'''


class TTraccar():
    def __init__(self):
        self.Url = 'http://192.168.2.208:8082/'
        self.Token = 'f5d451d2-0f7b-44ab-bde5-8ec4eb821f17'

    @staticmethod
    def HasCyrillic(aText):
        return bool(re.search('[а-яА-Я]', aText))

    async def send_message(self, aPhone: str, aMsg: str):
        Headers = {
            'Content-Type': 'application/json',
            'Authorization': self.Token
        }

        Payload = {
            'to': aPhone,
            'message': aMsg
        }

        async with aiohttp.ClientSession() as Session:
            async with Session.post(self.Url, json=Payload, headers=Headers) as Response:
                print(f'Phone:{aPhone}, Status: {Response.status}')

async def Main1():
    Dbl = TDbList(
        ['phone', 'name'],
        [
            ['-+380974274859', 'Ольга'],
            ['+380976646510', 'Володимир'],
            ['-+380677697216', 'Богдан'],
        ]
    )

    Traccar = TTraccar()
    for Rec in Dbl:
        Text = FmtText.format(Name=Rec.name)
        Phone = Rec.phone
        if (not Rec.phone.startswith('-')):
            await Traccar.send_message(Phone, Text)
            await asyncio.sleep(1)

async def Main2():
    Phone = '0976646510'
    Text = [
        "(1/3) Hello! Це змішане повідомлення з латиницею і кирилицею. Ми",
        "(2/3) хочемо зберегти цілі слова та правильні межі частин SMS. І",
        "(3/3) також додати маркери частин."
    ]

    Traccar = TTraccar()
    for xText in Text:
        await Traccar.send_message(Phone, xText)
        await asyncio.sleep(0.5)

async def Main():
    Phone = '0976646510'
    Text = FmtText.format(Name='Володимир')
    Traccar = TTraccar()
    await Traccar.send_message(Phone, Text)

asyncio.run(Main())
