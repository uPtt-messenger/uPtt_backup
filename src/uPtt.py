
import time
import threading

import log
import websocketserver
from config import Config
from command import Command
from pttadapter import PTTAdapter


if __name__ == '__main__':

    running = threading.Event()
    running.set()

    ConfigObj = Config()
    CommObj = Command()

    log.showValue(
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
        '終止程序完成'
    )
