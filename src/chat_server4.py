
import asyncio
import json
from aiohttp import web
from telethon import TelegramClient, events, functions, types
from telethon.tl.functions.channels import CreateChannelRequest
from telethon.tl.functions.messages import GetDialogFiltersRequest, UpdateDialogFilterRequest
from telethon.tl.types import DialogFilter

API_ID = 27489309
API_HASH = "aa5afcef4665d19b80710ef1d9ce9b46"

# WebSocket clients
clients = {}
user_groups = {}  # user_id -> group_id

# Telegram client
Client = TelegramClient("vlad", API_ID, API_HASH)

def GetChannelName(aId: int) -> str:
    return f'fw_chat_{aId}'

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

async def ChannelFind(aName: str) -> int:
    async for xDialog in Client.iter_dialogs():
        if (xDialog.is_channel) and (xDialog.entity.title == aName):
            return xDialog.entity.id

async def ChannelCreate(aName: str) -> int:
    Res = await ChannelFind(aName)
    if (not Res):
        group = await Client(CreateChannelRequest(
            title=aName,
            about='FindWares web-chat',
            megagroup=False
        ))
        Res= group.chats[0].id
    return int(f'-100{Res}')

async def websocket_handler(aRequest):
    ws = web.WebSocketResponse()
    await ws.prepare(aRequest)

    user_id = None
    async for xMsg in ws:
        if (xMsg.type == web.WSMsgType.TEXT):
            data = json.loads(xMsg.data)

            if (data['type'] == 'onopen'):
                user_id = data['user_chat']['id']
                clients[user_id] = ws

                group_id = user_groups.get(user_id)
                if (not group_id):
                    Name = GetChannelName(user_id)
                    group_id = await ChannelFind(Name)
                    if (group_id):
                        Messages = [
                            xMessage.text
                            async for xMessage in Client.iter_messages(group_id)
                            if xMessage.text
                        ]
                        await ws.send_json({
                            'type': 'onopen',
                            'messages': Messages
                        })

            elif (data['type'] == 'message') and user_id:
                message = data['message']

                #q1 = await CreateFolder(Client, 'myFolder')
                group_id = user_groups.get(user_id)
                if (not group_id):
                    Name = GetChannelName(user_id)
                    group_id = await ChannelCreate(Name)
                    user_groups[user_id] = group_id
                    Client.add_event_handler(handle_reply, events.NewMessage(chats=group_id))

                    # for user in group.users:
                    #     await Client.send_message(user.id, f'new group created {user_id}')

                    me = await Client.get_me()
                    await Client.send_message(me.id, f'new group created {user_id}')

                await Client.send_message(group_id, f'~{message}')
                print(f'got {message}')

    if user_id and user_id in clients:
        del clients[user_id]

    return ws

async def handle_reply(event):
    user_id = next((uid for uid, gid in user_groups.items() if gid == event.chat_id), None)
    if (user_id) and (user_id in clients):
        await clients[user_id].send_json({
            'type': 'handled',
            'message': event.message.text
        })

async def start_bot():
    print("Starting Telegram")
    await Client.start()
    if not Client.is_connected():
        await Client.connect()
    print("Bot started.")


async def main():
    await start_bot()
    app = web.Application()
    app.router.add_get("/ws", websocket_handler)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()
    print("WebSocket server started at ws://0.0.0.0:8080/ws")
    await Client.run_until_disconnected()  # Telegram не блокує основний потік


if __name__ == "__main__":
    asyncio.run(main())
