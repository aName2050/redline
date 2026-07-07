"""
Redline Communication Protocol
Raw bytes over UDP
v1.0
"""
# this file outlines the custom protocol for our super cool robot

# basic configs
PROTOCOL_VERSION = 1
HOST_NAME = "REDLINE"
UDP_PORT = 5800
MAX_PACKET_SIZE = 512
MAX_SEQUENCE = 0xFFFF

CONTROL_HZ = 50
TELEMETRY_HZ = 20

CONTROL_PERIOD_MS = 20
TELEMETRY_PERIOD_MS = 50
PING_PERIOD_MS = 1000
HEARTBEAT_PERIOD_MS = 100

WATCHDOG_TIMEOUT_MS = 250

# Packet types
PACKET_CONTROL = 0x01
PACKET_TELEMETRY = 0x02
PACKET_PING = 0x03
PACKET_HEARTBEAT = 0x04 # the robot is alive :O
PACKET_DISCOVERY_REQUEST = 0x05
PACKET_DISCOVERY_REPLY = 0x06

# Robot states
ROBOT_DISABLED = 0x00
ROBOT_ENABLED = 0x01
ROBOT_ESTOP = 0x02

# flags
FLAG_NONE = 0x00
FLAG_ENABLE = 1 << 0
FLAG_ESTOP = 1 << 1

# robot security (we dont want randoms connecting to the robot cuz that would be bad)
MAX_DRIVER_COUNT = 1