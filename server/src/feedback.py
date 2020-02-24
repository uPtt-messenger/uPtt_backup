import threading
import time
from msg import Msg


class Feedback:
    def __init__(self, console_obj):
        self.console = console_obj

        self.close = False
        self.closed = False

        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def event_close(self):
        self.close = True

        while True:
            if self.closed:
                break
            time.sleep(0.5)

    def run(self):
        while not self.close:
            

        self.closed = True
