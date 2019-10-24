

import logging
from websocket_server import WebsocketServer

import threading
import time


def new_client(client, server):
    server.send_message_to_all("Hey all, a new client has joined us")


def threadingsend(client, server, msg):
    for i in range(5):
        time.sleep(1)
        server.send_message(client, f'Echo [{msg}][{i}]')


def MessageReceived(client, server, msg):
    print(client)
    print(f'Receive [{msg}]')
    server.send_message(client, f'Echo [{msg}]')
    t = threading.Thread(target=threadingsend, args=(client, server, msg))
    t.daemon = True
    t.start()


if __name__ == '__main__':
    server = WebsocketServer(13254, host='127.0.0.1')
    # server.set_fn_new_client(new_client)
    server.set_fn_message_received(MessageReceived)
    server.run_forever()
