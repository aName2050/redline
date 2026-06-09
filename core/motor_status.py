import neopixel
import machine
import time

_GREEN = (0, 255, 0) # FORWARD
_RED = (255, 0, 0) # REVERSE
_BLUE = (0, 0, 255) # STALL
_WHITE = (255, 255, 255)
_OFF = (0, 0, 0)

class MotorStatusLED:
    LEFT = 0
    RIGHT = 1
    _DEADBAND = 0.05

    def __init__(self, pin: int = 22, num_pixels: int = 2, brightness: float = 0.5) -> None:
        self.pixels = neopixel.NeoPixel(machine.Pin(pin), num_pixels)
        self.brightness = max(0.0, min(1.0, brightness))
        self.disabled = False

        self._setPixel(self.LEFT, *_OFF)
        self._setPixel(self.RIGHT, *_OFF)

    def update(self, left_speed: float, right_speed: float) -> None:
        if self.disabled:
            return

        self._setPixel(self.LEFT, *self._speedToColor(left_speed))
        self._setPixel(self.RIGHT, *self._speedToColor(right_speed))
        self.pixels.write()

    def setDisabled(self) -> None:
        self.disabled = True
        self._setPixel(self.LEFT, *_OFF)
        self._setPixel(self.RIGHT, *_OFF)
        self.pixels.write()

    def setEnabled(self) -> None:
        self.disabled = False

    def setBrightness(self, brightness: float) -> None:
        self.brightness = max(0.0, min(1.0, brightness))

    def setColor(self, index: int, r: int, g: int, b: int) -> None:
        self._setPixel(index, r, g, b)
        self.pixels.write()

    # internal
    def _speedToColor(self, speed: float) -> tuple:
        if abs(speed) < self._DEADBAND:
            return _OFF
        elif speed > 0.0:
            return _GREEN
        else:
            return _RED

    def _setPixel(self, index: int, r: int, g: int, b: int) -> None:
        self.pixels[index] = (
            int(r * self.brightness),
            int(g * self.brightness),
            int(b * self.brightness)
        )