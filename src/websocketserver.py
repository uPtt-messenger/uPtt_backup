from websocket_server import WebsocketServer

import threading
import time

import Log

RunServer = True
ClientList = []


def ClientJoin(client, server):
    global ClientList
    ClientList.append(client)


def ClientLeave(client, server):
    global ClientList
    ClientList.remove(client)


def Send(client, server, msg):
    global ClientList
    if client not in ClientList:
        return
    
    # print(client['address'])
    try:
        Log.showValue(
            'WebSocket Server',
            Log.Level.INFO,
            '送出訊息',
            msg
        )
        server.send_message(client, msg)
    except BrokenPipeError:
        pass


def threadingsend(client, server, msg):
    for i in range(5):
        time.sleep(1)
        Send(client, server, f'Echo [{msg}][{i}]')


def MessageReceived(client, server, msg):
    print(client['address'])
    print(f'Receive [{msg}]')

    server.send_message(client, f'Echo [{msg}]')


def ServerSetup():
    Log.showValue(
        'WebSocket Server',
        Log.Level.INFO,
        '啟動伺服器',
        50730
    )
    server = WebsocketServer(50730, host='127.0.0.1')
    server.set_fn_new_client(ClientJoin)
    server.set_fn_client_left(ClientLeave)
    server.set_fn_message_received(MessageReceived)
    server.run_forever()


def start():
    t = threading.Thread(target=ServerSetup)
    t.daemon = True
    t.start()


if __name__ == '__main__':
    start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print('關閉 WebSocket Server')
            break
