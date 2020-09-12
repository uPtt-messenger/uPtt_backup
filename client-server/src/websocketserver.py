import asyncio
import websockets
import traceback
import time
import threading
import json

from util.src.log import Logger
from util.src.msg import Msg


class WsServer:

    def __init__(self, console_obj):

        self.console = console_obj

        self.logger = Logger('WS', Logger.INFO)
        self.thread = None
        self.start_error = False
        self.run_session = True
        self.run = True
        self.server_start = False

    def start(self):
        self.thread = threading.Thread(
            target=self.server_setup,
            daemon=True)
        self.thread.start()
        time.sleep(2)
        if self.start_error:
            self.logger.show(
                Logger.INFO,
                '啟動失敗')
        else:
            self.logger.show(
                Logger.INFO,
                '啟動成功')

    def stop(self):

        self.logger.show(
            Logger.INFO,
            '執行終止程序')

        while not self.server_start:
            time.sleep(0.1)

        self.run_session = False
        self.run = False
        # thread.join()
        self.logger.show(
            Logger.INFO,
            '終止程序完成')

    async def consumer_handler(self, ws, path):

        while self.run_session:
            try:
                try:
                    recv_msg_str = await ws.recv()
                except Exception as e:
                    print('Connection Close: recv fail')
                    raise ValueError('Connection Close: recv fail')

                self.logger.show_value(
                    Logger.INFO,
                    '收到字串',
                    recv_msg_str)
                self.logger.show_value(
                    Logger.INFO,
                    '路徑',
                    path)

                try:
                    recv_msg = Msg(strobj=recv_msg_str)
                except json.JSONDecodeError:
                    self.logger.show_value(
                        Logger.INFO,
                        '丟棄錯誤訊息',
                        recv_msg_str)
                    self.run_session = False
                    break

                if 'token=' in path:
                    token = path[path.find('token=') + len('token='):]
                    if '&' in token:
                        token = token[:token.find('&')]
                    self.logger.show_value(
                        Logger.INFO,
                        '收到權杖',
                        token)
                    recv_msg.add(Msg.key_token, token)

                # print(str(recv_msg))
                self.console.command.analyze(recv_msg)
                # await ws.send(recv_msg)
                # print(f'echo complete')
            except Exception as e:
                traceback.print_tb(e.__traceback__)
                print(e)
                print('Connection Close')
                self.run_session = False
                break

    async def producer_handler(self, ws, path):

        while self.run_session:
            while self.console.command.push_msg:
                push_msg = self.console.command.push_msg.pop()

                print(f'push [{push_msg}]')
                try:
                    await ws.send(push_msg)
                except websockets.exceptions.ConnectionClosedOK:
                    print(f'push fail')
                    break
            await asyncio.sleep(0.1)

    async def handler(self, websocket, path):
        while self.run_session:
            consumer_task = asyncio.ensure_future(
                self.consumer_handler(websocket, path))

            producer_task = asyncio.ensure_future(
                self.producer_handler(websocket, path))

            _, pending = await asyncio.wait(
                [consumer_task, producer_task],
                return_when=asyncio.FIRST_COMPLETED)
            for task in pending:
                task.cancel()

        self.run_session = self.run

    def server_setup(self):
        logger = Logger('WS', Logger.INFO)

        logger.show_value(
            Logger.INFO,
            '啟動伺服器',
            f'ws://127.0.0.1:{self.console.config.port}')

        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)

        start_server = websockets.serve(
            self.handler,
            "localhost",
            self.console.config.port,
        )


        try:
            asyncio.get_event_loop().run_until_complete(start_server)
        except OSError:
            self.start_error = True

        if self.start_error:
            return

        self.server_start = True

        asyncio.get_event_loop().run_forever()

        logger.show(
            Logger.INFO,
            '關閉伺服器')


if __name__ == '__main__':
    start()
    # stop()

    while True:
        try:
            time.sleep(1)
        except Exception:
            stop()
            break
