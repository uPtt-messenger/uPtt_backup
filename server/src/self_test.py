import sys
import asyncio
import websockets
import json

import log
from config import Config
from msg import Msg

msg_str = None
recv_msg = None


async def ws_send():
    global msg_str
    global recv_msg
    global config
    uri = f"ws://localhost:{config.port}"
    async with websockets.connect(uri) as ws:
        await ws.send(msg_str)
        recv_msg_str = await ws.recv()
        recv_msg = Msg(strobj=recv_msg_str)


def send(msg: Msg):
    global msg_str
    msg_str = str(msg)
    asyncio.get_event_loop().run_until_complete(ws_send())


def get_password(password_file):
    try:
        with open(password_file) as AccountFile:
            account = json.load(AccountFile)
            ptt_id = account['ID']
            password = account['Password']
    except FileNotFoundError:
        print('Please note PTT ID and Password in Account.txt')
        print('{"ID":"YourID", "Password":"YourPassword"}')
        sys.exit()

    return ptt_id, password


config = Config()

log.show_value(
    '自我測試',
    log.level.INFO,
    'uPtt 版本',
    config.version
)

ptt_id, ptt_pw = get_password('account.txt')

payload = Msg()
payload.add(Msg.key_ptt_id, ptt_id)
payload.add(Msg.key_ptt_pass, ptt_pw)

push_msg = Msg(operate=Msg.key_login)

push_msg.add(Msg.key_payload, payload)

send(push_msg)



logout_msg = Msg(operate=Msg.key_logout)
send(logout_msg)

close_msg = Msg(operate=Msg.key_close)
send(close_msg)