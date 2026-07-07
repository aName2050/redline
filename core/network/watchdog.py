import time
import core.network.protocol as protocol

class Watchdog:
    def __init__(self):
        self._lastFeed = time.ticks_ms()

    def feed(self) -> None:
        self._lastFeed = time.ticks_ms()

    def reset(self) -> None:
        self.feed()

    def elapsed(self) -> int:
        return time.ticks_diff(time.ticks_ms(), self._lastFeed)

    def isAlive(self) -> bool:
        return self.elapsed() <= protocol.WATCHDOG_TIMEOUT_MS

    def hasTimedOut(self) -> bool:
        return not self.isAlive()