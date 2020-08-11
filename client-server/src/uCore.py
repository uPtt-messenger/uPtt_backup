import os
import sys
import time
import threading

import log
import websocketserver
from config import Config
from command import Command
from pttadapter import PTT_Adapter
from feedback import Feedback
from event import EventConsole
from console import Console
from dynamic_data import DynamicData
from black_list import BlackList

LogPath = None


def log_to_file(msg):
    global LogPath
    if LogPath is None:
        desktop = os.path.join(
            os.path.join(
                os.environ['USERPROFILE']
            ),
            'Desktop'
        )

        LogPath = f'{desktop}/uPttLog.txt'

        print(LogPath)

    with open(LogPath, 'a', encoding='utf8') as f:
        f.write(f'{msg}\n')


if __name__ == '__main__':

    config_obj = Config()

    console_obj = Console()
    console_obj.config = config_obj

    log.show_value(
        'uCore',
        log.level.INFO,
        'uPtt 版本',
        config_obj.version
    )

    if len(sys.argv) > 1:
        print(sys.argv)

    if '-debug' in sys.argv or '-trace' in sys.argv:
        log.Handler = log_to_file
        config_obj.LogHandler = log_to_file

    if '-trace' in sys.argv:
        config_obj.LogHandler = log.level.TRACE

    if '-dev' in sys.argv:
        console_obj.run_mode = 'dev'

    log.show_value(
        'uCore',
        log.level.INFO,
        '執行模式',
        console_obj.run_mode
    )

    event_console = EventConsole()
    console_obj.event = event_console

    dynamic_data_obj = DynamicData(console_obj)
    console_obj.dynamic_data = dynamic_data_obj

    comm_obj = Command(console_obj)
    console_obj.command = comm_obj

    black_list = BlackList(console_obj)

    feedback = Feedback(console_obj)
    ptt_adapter = PTT_Adapter(console_obj)

    # websocketserver 是特例
    websocketserver.config = config_obj
    websocketserver.command = comm_obj

    run_server = True
    def event_close():
        global run_server
        run_server = False

    event_console.close.append(websocketserver.stop)
    event_console.close.append(event_close)

    websocketserver.start()

    if websocketserver.start_error:
        log.show(
            'uCore',
            log.level.INFO,
            'websocket app-server startup error'
        )
        for e in event_console.close:
            e()
    else:
        while run_server:
            try:
                time.sleep(0.5)
            except KeyboardInterrupt:
                for e in event_console.close:
                    e()
                break

    log.show(
        'uCore',
        log.level.INFO,
        '執行最終終止程序')

    running = threading.Event()
    running.set()
    running.clear()

    log.show(
        'uCore',
        log.level.INFO,
        '最終終止程序全數完成'
    )
