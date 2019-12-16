
import time

import Log
import Config
import websocketserver

if __name__ == '__main__':

    ConfigObj = Config.Config()

    Log.showValue(
        'Main',
        Log.Level.INFO,
        'uPtt 版本',
        ConfigObj.Version
    )

    websocketserver.start()
    while websocketserver.RunServer:
        try:
            time.sleep(10)
        except KeyboardInterrupt:
            Log.show(
                'Main',
                Log.Level.INFO,
                '伺服器關閉'
            )
            break
