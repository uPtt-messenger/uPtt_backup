import threading
import time

from util.src import log


class Feedback:
    def __init__(self, console_obj):
        self.console = console_obj

        console_obj.event.close.append(self.event_close)

        self.close = False
        self.closed = False

        self.thread = threading.Thread(
            target=self.run,
            daemon=True)
        self.thread.start()

    def event_close(self):
        log.show(
            'Feedback',
            log.level.INFO,
            '執行終止程序'
        )
        self.close = True
        self.thread.join()

        log.show(
            'Feedback',
            log.level.INFO,
            '終止程序完成'
        )
        #
        # while True:
        #     if self.closed:
        #         break
        #     time.sleep(self.console.config.quick_response_time)

    def run(self):

        while not self.close:

            log.show(
                'Feedback',
                log.level.INFO,
                '更新上線狀態')

            start_time = end_time = time.time()
            while end_time - start_time < self.console.config.feedback_frequency:
                time.sleep(self.console.config.quick_response_time)
                end_time = time.time()

                if self.close:
                    break
