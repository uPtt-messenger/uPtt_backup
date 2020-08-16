import threading
import time

from util.src.log import Logger


class Feedback:
    def __init__(self, console_obj):
        self.console = console_obj
        
        self.logger = Logger('FeedBack', Logger.INFO)

        console_obj.event.close.append(self.event_close)

        self.close = False
        self.closed = False

        self.thread = threading.Thread(
            target=self.run,
            daemon=True)
        self.thread.start()

    def event_close(self):
        self.logger.show(
            Logger.INFO,
            '執行終止程序')
        self.close = True
        self.thread.join()

        self.logger.show(
            Logger.INFO,
            '終止程序完成')
        #
        # while True:
        #     if self.closed:
        #         break
        #     time.sleep(self.console.config.quick_response_time)

    def run(self):

        while not self.close:

            self.logger.show(
                Logger.INFO,
                '更新上線狀態')

            start_time = end_time = time.time()
            while end_time - start_time < self.console.config.feedback_frequency:
                time.sleep(self.console.config.quick_response_time)
                end_time = time.time()

                if self.close:
                    break
