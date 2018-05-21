import threading

class WStoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, target):
        super(WStoppableThread, self).__init__(target=target)
        self.continue_thread = True
        print(self.continue_thread)

    def stop(self):
        self.continue_thread = False

    def stopped(self):
        return not self.continue_thread

