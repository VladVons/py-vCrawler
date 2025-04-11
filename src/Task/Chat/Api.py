# Created: 2024.05.07
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import json
from aiohttp import web
from telethon import TelegramClient, events
from telethon.tl.functions.channels import CreateChannelRequest
from telethon.tl.functions.messages import GetDialogFiltersRequest, UpdateDialogFilterRequest
from telethon.tl.types import DialogFilter
from telethon.errors import ChannelPrivateError
from Inc.DataClass import DDataClass
from IncP.ApiBase import TApiBase
from IncP.Log import Log

@DDataClass
class TApiChatConf():
    id: int
    hash: str
    session: str


class TApiChat(TApiBase):
    def __init__(self):
        super().__init__()

        Conf = self.GetConf()
        self.Conf = TApiChatConf(**Conf)

        self.clients = {}
        self.user_groups = {}  # user_id -> group_id
        self.Client: TelegramClient = None

    @staticmethod
    def GetChannelName(aId: int) -> str:
        return f'fw_chat_{aId}'

    async def InitA(self):
        Log.Print(1, 'i', f'TelegramClient(). id: {self.Conf.id}, hash: ...{self.Conf.hash[-8:]}')

        self.Client = TelegramClient(self.Conf.session, self.Conf.id, self.Conf.hash)
        await self.Client.start()
        if (not self.Client.is_connected()):
            await self.Client.connect()

        Me = await self.Client.get_me()
        Log.Print(1, 'i', f'Session phone: {Me.phone}')

    async def GetMessages(self, aGroupId: int) -> list:
        Res = [
            {
                'date': xMessage.date.astimezone().strftime('%Y-%m-%d %H:%M:%S'),
                'text': xMessage.text
            }
            async for xMessage in self.Client.iter_messages(aGroupId, limit=100)
            if xMessage.text
        ]
        Res.reverse()
        return Res

    async def HandleReply(self, event):
        user_id = next((uid for uid, gid in self.user_groups.items() if gid == event.chat_id), None)
        if (user_id) and (user_id in self.clients):
            await self.clients[user_id].send_json({
                'type': 'handled',
                'text': event.message.text,
                'date': event.message.date.astimezone().strftime('%Y-%m-%d %H:%M:%S')
            })

    async def Handle(self, aRequest):
        ws = web.WebSocketResponse()
        try:
            await ws.prepare(aRequest)
        except Exception as E:
            Log.Print(1, 'e', f'prepare() {E}')
            return web.Response(text="Unexpected error", status=500)

        user_id = None
        async for xMsg in ws:
            if (xMsg.type == web.WSMsgType.TEXT):
                data = json.loads(xMsg.data)

                if (data['type'] == 'onopen'):
                    user_id = data['user_chat']['id']
                    self.clients[user_id] = ws

                    group_id = self.user_groups.get(user_id)
                    if (not group_id):
                        Name = self.GetChannelName(user_id)
                        group_id = await self.ChannelFind(Name)
                        self.user_groups[user_id] = group_id

                    if (group_id):
                        try:
                            Messages = await self.GetMessages(group_id)
                            await ws.send_json({
                                'type': 'onopen',
                                'messages': Messages
                            })
                        except ChannelPrivateError: # possible deleted
                            del self.user_groups[user_id]

                elif (data['type'] == 'message') and user_id:
                    message = data['message']

                    #q1 = await CreateFolder(Client, 'myFolder')
                    group_id = self.user_groups.get(user_id)
                    if (not group_id):
                        Name = self.GetChannelName(user_id)
                        group_id = await self.ChannelCreate(Name)
                        self.user_groups[user_id] = group_id
                        self.Client.add_event_handler(self.HandleReply, events.NewMessage(chats=group_id))

                        # for user in group.users:
                        #     await Client.send_message(user.id, f'new group created {user_id}')

                        me = await self.Client.get_me()
                        await self.Client.send_message(me.id, f'new group created {user_id}')

                    await self.Client.send_message(group_id, f'~{message}')
                    print(f'got {message}')
                pass

        if (user_id) and (user_id in self.clients):
            del self.clients[user_id]

        return ws

    @staticmethod
    async def CreateFolder(aClient, aName: str):
        def _CheckExists(aFilters: list) -> bool:
            for xFilter in aFilters:
                if (isinstance(xFilter, DialogFilter)):
                    if (xFilter.title.text == aName):
                        return True

        current_filters = await aClient(GetDialogFiltersRequest())
        if (not _CheckExists(current_filters.filters)):
            new_filter = DialogFilter(
                id=0,
                title=aName,
                pinned_peers=[],
                include_peers=[],
                exclude_peers=[]
            )
            q1 = UpdateDialogFilterRequest(id=0, filter=new_filter)
            await aClient(q1)

    async def ChannelFind(self, aName: str) -> int:
        async for xDialog in self.Client.iter_dialogs():
            if (xDialog.is_channel) and (xDialog.entity.title == aName):
                return xDialog.entity.id

    async def ChannelCreate(self, aName: str) -> int:
        Res = await self.ChannelFind(aName)
        if (not Res):
            group = await self.Client(CreateChannelRequest(
                title=aName,
                about='FindWares web-chat',
                megagroup=False
            ))
            Res= group.chats[0].id
        return int(f'-100{Res}')

ApiChat = TApiChat()
