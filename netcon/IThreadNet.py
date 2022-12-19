from threading import Thread
from Event import Event


class IThreadNet:
    EVENT_START: Event = Event()
    WORK: bool = True
    PAUSE: bool = False
    EVENT_STOP: Event = Event()
    _run = (_ for _ in range(0))

    def stop(self):
        self.WORK = False

    def start(self):
        self._run = self.__run()
        Thread(target=lambda: next(self._run), daemon=True).start()
        self.EVENT_START.invoke(self)

    def resume(self):
        self.PAUSE = False
        Thread(target=lambda: next(self._run), daemon=True).start()

    def pause(self):
        self.PAUSE = True

    def __run(self):
        yield 0
        self.EVENT_STOP.invoke()
