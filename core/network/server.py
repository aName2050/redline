import socket
import select
import uasyncio as asyncio
from core.network.packet import Packet
from core.network.watchdog import Watchdog
import core.network.protocol as protocol

class Server:
    def __init__(self) -> None:
        self._socket = None
        self._poll = select.poll()
        self._watchdog = Watchdog()
        self._driver = None # controller ip and port
        self._control = None # latest valid command packet
        self._sequence = 0
        self._running = False

    def start(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind(("0.0.0.0", protocol.UDP_PORT))
        self._socket.setblocking(False)

        self._poll.register(self._socket, select.POLLIN)

        self._running = True
        print(f"[Server] Listening on UDP/{protocol.UDP_PORT}")

    def stop(self):
        self._running = False

        if self._socket:
            self._poll.unregister(self._socket)
            self._socket.close()
            self._socket = None

        self._driver = None
        self._control = None

        print("[Server] Stopped")

    def isConnected(self) -> bool:
        return self._driver is not None

    def getDriver(self):
        return self._driver

    def getControl(self):
        return self._control

    def getWatchdog(self):
        self._watchdog

    # send packets
    def _send(self, data: bytes, address):
        self._socket.sendto(data, address) # type: ignore

    def _sendDiscoveryReply(self, address):
        packet = Packet.encodeDiscoveryReply(
            flags=0,
            sequence=self._sequence,
            port=protocol.UDP_PORT,
            robotName=protocol.HOST_NAME
        )

        self._send(packet, address)
        self._sequence += 1
        if self._sequence > protocol.MAX_SEQUENCE:
            self._sequence = 0

    # handle packets
    def _handleDiscovery(self, address):
        self._sendDiscoveryReply(address)

    def _claimDriver(self, address):
        if self._driver is None:
            self._driver = address
            print(f"[Server] Driver connected: {address}")

    def _releaseDriver(self):
        if self._driver is not None:
            print(f"[Server] Driver disconnected: {self._driver}")

        self._driver = None
        self._control = None

    def _handleControl(self, packet, address):
        self._claimDriver(address)

        if address != self._driver:
            return

        self._control = packet
        self._watchdog.feed()

    def _handleHeartbeat(self, address):
        if address == self._driver:
            self._watchdog.feed()

    # main loop
    async def update(self):
        while self._running:
            # watchdog timer
            if self._driver and self._watchdog.hasTimedOut():
                self._releaseDriver()

            events = self._poll.poll(0)

            for sock, event in events:
                if not (event & select.POLLIN):
                    continue

                try:
                    data, address = self._socket.recvfrom(protocol.MAX_PACKET_SIZE) # type: ignore
                except OSError:
                    continue

                try:
                    header = Packet.decodeHeader(data)
                except Exception:
                    continue

                packetType = header["type"]

                if packetType == protocol.PACKET_DISCOVERY_REQUEST:
                    self._handleDiscovery(address)
                elif packetType == protocol.PACKET_CONTROL:
                    try:
                        packet = Packet.decodeControl(data)
                        self._handleControl(packet, address)
                    except Exception:
                        pass
                elif packetType == protocol.PACKET_HEARTBEAT:
                    self._handleHeartbeat(address)

            await asyncio.sleep_ms(1)