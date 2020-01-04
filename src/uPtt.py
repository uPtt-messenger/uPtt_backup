
import os
import sys
import time
import threading

import log
import websocketserver
from config import Config
from command import Command
from pttadapter import PTTAdapter

LogPath = None


def log2File(Msg):
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

    running = threading.Event()
    running.set()

    ConfigObj = Config()
    CommObj = Command()

    print(sys.argv)

    if '-debug' in sys.argv or '-trace' in sys.argv:
        log.Handler = log2File
        ConfigObj.LogHandler = log2File
    
    if '-trace' in sys.argv:
        ConfigObj.LogHandler = log.Level.TRACE

    log.showvalue(
        'Main',
        log.Level.INFO,
        'uPtt 版本',
        ConfigObj.Version
    )

    pttadapter = PTTAdapter(ConfigObj, CommObj)

    websocketserver.Config = ConfigObj
    websocketserver.Command = CommObj
    websocketserver.start()
    while not CommObj.close:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            break

    log.show(
        'Main',
        log.Level.INFO,
        '執行終止程序'
    )
    pttadapter.stop()
    websocketserver.stop()

    # 清除所有潛在
    running.clear()

    log.show(
        'Main',
        log.Level.INFO,
        '全部終止程序完成'
    )
