from threading import Thread
from time import sleep


class DelayTimerThread(Thread):

    _FREQUENCY_HZ = 60

    def __init__(self, memory):
        Thread.__init__(self)
        self.memory = memory

    def run(self):
        while True:
            self.memory.decrement_delay_timer()
            sleep(1 / self._FREQUENCY_HZ)
