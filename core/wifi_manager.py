import network
import time

# CONFIG
# pls dont steal my wifi creds :(
SSID = "REDLINE"
PASSWORD = "RL-2040-XBEE"
IP = "172.31.255.1"
SUBNET = "255.255.255.0"
GATEWAY = "172.31.255.1"
DNS = "172.31.255.1"
CHANNEL = 6

class WiFiManager:
    def __init__(self, status_led=None) -> None:
        self._led = status_led
        self._ap = network.WLAN(network.AP_IF)

    def start(self) -> bool:
        self._setLED("wifi_connect")
        print("[WiFiManager] Starting 2.4GHz wireless AP...")

        self._ap.active(True)
        self._ap.config(
            ssid = SSID,
            password = PASSWORD,
            channel = CHANNEL,
            security = 4 # WPA2-PSK
        )

        self._ap.ifconfig((IP, SUBNET, GATEWAY, DNS))

        print("[WiFiManager] Waiting for AP to start...")

        start = time.ticks_ms()
        while not self._ap.active():
            if time.ticks_diff(time.ticks_ms(), start) > 5000:
                print("[WiFiManager] ERR_TIMEOUT: AP failed to start")
                self._setLED("fault")
                return False
            if self._led:
                self._led.updateLED()
            time.sleep_ms(50)

        print("[WiFiManager] It's alive!!! :D")
        print(f"[WiFiManager] SSID: {SSID}")
        print(f"[WiFiManager] IP: {IP}")
        print(f"[WiFiManager] PASSWORD: {PASSWORD}")
        print(f"[WiFiManager] CHANNEL: {CHANNEL}")
        self._setLED("wifi_connected")
        return True

    def stop(self) -> None:
        self._ap.active(False)
        print("[WiFiManager] AP stopped")

    def isActive(self) -> bool:
        return self._ap.active()

    def getIP(self) -> str:
        return IP

    def getSSID(self) -> str:
        return SSID

    def getClientCount(self) -> int:
        # i dunno why this throws an error, copied it straight from the docs.
        # i'll find out one day though
        return len(self._ap.status("stations")) # type: ignore

    def hasClient(self) -> bool:
        return self.getClientCount() > 0

    # internal
    def _setLED(self, state: str) -> None:
        if self._led:
            self._led.setState(state)