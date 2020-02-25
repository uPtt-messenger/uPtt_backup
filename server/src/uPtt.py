
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

LogPath = None


def log_to_file(Msg):
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
        f.write(f'{Msg}\n')


if __name__ == '__main__':

    config_obj = Config()

    event_console = EventConsole()
    comm_obj = Command(event_console)

    console_obj = Console(config_obj, comm_obj, event_console)

    if len(sys.argv) > 1:
        print(sys.argv)

    if '-debug' in sys.argv or '-trace' in sys.argv:
        log.Handler = log_to_file
        config_obj.LogHandler = log_to_file
    
    if '-trace' in sys.argv:
        config_obj.LogHandler = log.level.TRACE

    log.show_value(
        'Main',
        log.level.INFO,
        'uPtt 版本',
        config_obj.version
    )

    feedback = Feedback(console_obj)
    ptt_adapter = PTT_Adapter(console_obj)

    # websocketserver 是特例
    websocketserver.config = config_obj
    websocketserver.command = comm_obj
    websocketserver.start()

    run_server = True

    def event_close():
        global run_server
        run_server = False


    event_console.close.append(websocketserver.stop)
    event_console.close.append(event_close)
    while run_server:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            for e in event_console.close:
                e()
            break

    log.show(
        'Main',
        log.level.INFO,
        '執行最終終止程序'
    )

    running = threading.Event()
    running.set()
    running.clear()

    log.show(
        'Main',
        log.level.INFO,
        '最終終止程序全數完成'
    )
