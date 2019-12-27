import time
import threading
import traceback

from PTTLibrary import PTT
import log


class PTTAdapter:
    def __init__(self, config, command):
        self.Config = config
        self.Command = command

        Thread = threading.Thread(
            target=self.run,
            daemon=True
        )
        Thread.start()

    def run(self):

        log.show(
            'PTTAdapter',
            log.Level.INFO,
            '啟動'
        )
        self.bot = PTT.Library()

        while True:
            
            StartTime = EndTime = time.time()
            while EndTime - StartTime < self.Config.QueryCycle:
                if (ID, Password := self.Command.recvlogin()) != (None, None):
                    log.show(
                        'PTTAdapter',
                        log.Level.INFO,
                        '執行登入'
                    )
                    log.showValue(
                        'PTTAdapter',
                        log.Level.INFO,
                        '帳號',
                        ID
                    )
                    log.showValue(
                        'PTTAdapter',
                        log.Level.INFO,
                        '密碼',
                        Password
                    )
                
                time.sleep(0.05)
                EndTime = time.time()
                
