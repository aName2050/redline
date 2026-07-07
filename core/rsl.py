from machine import Pin, PWM
import time

_ORANGE = (255, 126, 0)
_RED = (255, 0, 0)
_OFF = (0, 0, 0)
_BLUE = (0, 0, 200)

class RSL:
    OFF = "off"
    DISABLED = "disabled"
    ENABLED = "enabled"
    ESTOP = "estop"
    ABORT = "abort"

    def __init__(self, pinR: int, pinG: int, pinB: int, freq: int = 1000) -> None:
        self.r = PWM(Pin(pinR))
        self.g = PWM(Pin(pinG))
        self.b = PWM(Pin(pinB))

        self.r.freq(freq)
        self.g.freq(freq)
        self.b.freq(freq)

        self.r.duty_u16(0)
        self.g.duty_u16(0)
        self.b.duty_u16(0)

        self.state = self.OFF
        self.led_on = False
        self.last_tick = time.ticks_ms()
        self.blink_ms = 450

        self._setColor(*_OFF)

    def setState(self, state: str) -> None:
        if state == self.state:
            return

        self.state= state
        self.last_tick = time.ticks_ms()
        self.led_on = False

        if state == self.OFF:
            self._setColor(*_OFF)
        elif state == self.DISABLED:
            self._setColor(*_ORANGE)
        elif state == self.ESTOP:
            self._setColor(*_RED)
        elif state == self.ABORT:
            self._setColor(*_BLUE)

    def getState(self) -> str:
        return self.state

    def update(self) -> None:
        if self.state != self.ENABLED:
            return

        now = time.ticks_ms()
        elapsed = time.ticks_diff(now, self.last_tick)

        if elapsed >= self.blink_ms:
            self.led_on = not self.led_on
            self.last_tick = now
            self._setColor(*(_ORANGE if self.led_on else _OFF))

    # internal
    def _setColor(self, r: int, g: int, b: int, brightness: float = 1.0) -> None:
        brightness = max(0.0, min(1.0, brightness))
        self.r.duty_u16(int(r * 257 * brightness))
        self.g.duty_u16(int(g * 257 * brightness))
        self.b.duty_u16(int(b * 257 * brightness))