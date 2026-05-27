import time
from machine import Pin

class StatusLED:
    BOOTING = "booting"
    WIFI_CONNECTING = "wifi_connect"
    WIFI_CONNECTED = "wifi_connected"
    ENABLED = "enabled"
    DISABLED = "disabled"
    FAULT = "fault"

    LED_PATTERNS = {
        BOOTING: {"pulses": [(80, 80), (80, 80)], "gap": 2000},
        WIFI_CONNECTING: {"pulses": [(500, 500)], "gap": 0},
        WIFI_CONNECTED: {"pulses": [(100, 100)], "gap": 0},
        ENABLED: {"pulses": None, "gap": 0},
        DISABLED: {"pulses": None, "gap": 0},
        FAULT: {"pulses": [(80, 80), (80, 80), (80, 80), (80, 80)],  "gap": 500}
    }

    def __init__(self) -> None:
        self._led = Pin("LED", Pin.OUT)
        self._state = self.BOOTING

        self.pulse_index = 0
        self.in_gap = False
        self.last_tick = time.ticks_ms()
        self.led_on = False

    def setState(self, state: str) -> None:
        if state == self._state:
            return

        self._state = state
        self.pulse_index = 0
        self.in_gap = False
        self.last_tick = time.ticks_ms()

        if state == self.ENABLED:
            self.led_on = True
            self._led.on()
        elif state == self.DISABLED:
            self.led_on = False
            self._led.off()

    def getState(self) -> str:
        return self._state

    def updateLED(self) -> None:
        pattern = self.LED_PATTERNS.get(self._state)
        if pattern is None:
            return

        pulses = pattern["pulses"]

        if pulses is None:
            return

        now = time.ticks_ms()
        elapsed = time.ticks_diff(now, self.last_tick)

        if self.in_gap:
            if elapsed >= pattern["gap"]:
                self.in_gap = False
                self.pulse_index = 0
                self.last_tick = now
            return

        if self.pulse_index >= len(pulses):
            if pattern["gap"] > 0:
                self.in_gap = True
                self.last_tick = now
            else:
                self.pulse_index = 0
                self.last_tick = now
            return

        on_ms, off_ms = pulses[self.pulse_index]
        total_ms = on_ms + off_ms

        if elapsed < on_ms:
            self._led.on()
        elif elapsed < total_ms:
            self._led.off()
        else:
            self.pulse_index += 1
            self.last_tick = now