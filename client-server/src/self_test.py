import sys
import asyncio
import websockets
import json
import time
from PyPtt import PTT

from backend_util.src.log import Logger
from config import Config
from backend_util.src.msg import Msg

msg_str = None
recv_msg = None
token = None
logger = Logger('自我測試', Logger.INFO)

async def ws_send():
    global msg_str
    global recv_msg
    global config
    global token

    if token is None:
        uri = f"ws://localhost:{config.port}"
    else:
        uri = f"ws://localhost:{config.port}?token={token}"
    async with websockets.connect(uri) as ws:
        logger.show_value(
            '自我測試',
            Logger.INFO,
            '準備送出',
            msg_str)
        await ws.send(msg_str)
        recv_msg_str = await ws.recv()
        logger.show_value(
            '自我測試',
            Logger.INFO,
            '收到',
            recv_msg_str)
        recv_msg = Msg(strobj=recv_msg_str)


def send(msg: Msg):
    global msg_str
    msg_str = str(msg)
    try:
        asyncio.get_event_loop().run_until_complete(ws_send())
    except websockets.exceptions.ConnectionClosedOK:
        logger.show(
            Logger.INFO,
            '連線關閉')


def recv():
    global recv_msg
    try:
        asyncio.get_event_loop().run_until_complete(ws_recv())
    except websockets.exceptions.ConnectionClosedOK:
        logger.show(
            Logger.INFO,
            '連線關閉')
        return None
    return recv_msg


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

logger.show_value(
    '自我測試',
    Logger.INFO,
    'uPtt 版本',
    config.version)

ptt_id, ptt_pw = get_password('account.txt')

payload = Msg()
payload.add(Msg.key_ptt_id, ptt_id)
payload.add(Msg.key_ptt_pass, ptt_pw)

push_msg = Msg(operate=Msg.key_login)

logger.show(
    Logger.INFO,
    '開始登入')

push_msg.add(Msg.key_payload, payload)
send(push_msg)

if recv_msg.data[Msg.key_code] != 0:
    logger.show(
        Logger.INFO,
        '登入失敗')
    sys.exit()

logger.show(
    Logger.INFO,
    '登入成功')

token = recv_msg.data['payload']['token']

logger.show_value(
    Logger.INFO,
    '收到權杖',
    token
)

time.sleep(3)
#################################

ptt_bot = PTT.API()
ptt_id2, ptt_pw2 = get_password('account2.txt')
try:
    ptt_bot.login(
        ptt_id2,
        ptt_pw2,
        kick_other_login=True)
except PTT.exceptions.LoginError:
    ptt_bot.log('登入失敗')
    sys.exit()
except PTT.exceptions.ConnectError:
    ptt_bot.log('登入失敗')
    sys.exit()
time.sleep(3)

logger.show(
    Logger.INFO,
    '準備丟水球'
)

test_msg = 'uPtt test waterball msg'
# ptt_bot.throw_waterball(ptt_id, test_msg)
#
# waterball_msg = recv()
# print(waterball_msg)

# {"operation":"sendwaterball","payload": {"pttId": "DeepLearning","content": "1234567"}}

for index in range(1):
    send_waterball_msg = Msg(operate=Msg.key_sendwaterball)
    payload = Msg()
    payload.add(Msg.key_ptt_id, ptt_id2)
    payload.add(Msg.key_content, f'{test_msg} {index}')
    send_waterball_msg.add(Msg.key_payload, payload)
    send(send_waterball_msg)

waterball_list = ptt_bot.get_waterball(PTT.data_type.waterball_operate_type.CLEAR)
test_send_waterball_result = False
for waterball in waterball_list:
    print(waterball.content)

    if test_msg in waterball.content:
        test_send_waterball_result = True

if test_send_waterball_result:
    logger.show(
        Logger.INFO,
        '丟水球測試成功')
else:
    logger.show(
        Logger.INFO,
        '丟水球測試失敗')

#################################

ptt_bot.logout()

logger.show(
    Logger.INFO,
    '準備登出')

logout_msg = Msg(operate=Msg.key_logout)
send(logout_msg)

logger.show(
    Logger.INFO,
    '登出成功'
)

logger.show(
    Logger.INFO,
    '準備關閉'
)

close_msg = Msg(operate=Msg.key_close)
send(close_msg)

logger.show(
    Logger.INFO,
    '關閉成功'
)
