
import threading

from msg import Msg

class Feedback:
    def __init__(self, console_obj):
        self.console = console_obj
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):

        pass

        # while not self.config.command.close:
        #
        #     while