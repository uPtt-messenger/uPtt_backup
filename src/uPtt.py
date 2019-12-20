
import time

import log
import websocketserver
from config import Config
from command import Command


if __name__ == '__main__':

    ConfigObj = Config()
    CommObj = Command()

    log.showValue(
        'Main',
        log.Level.INFO,
        'uPtt 版本',
        ConfigObj.Version
    )

    websocketserver.Command = CommObj
    websocketserver.start()
    while True:
        try:
            time.sleep(10)
        except KeyboardInterrupt:
            log.show(
                'Main',
                log.Level.INFO,
                '關閉伺服器'
            )
            websocketserver.stop()
            break
