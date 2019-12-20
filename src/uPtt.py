
import time

import log
import config
import websocketserver

if __name__ == '__main__':

    ConfigObj = config.Config()

    log.showValue(
        'Main',
        log.Level.INFO,
        'uPtt 版本',
        ConfigObj.Version
    )

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
