import struct
import core.network.protocol as protocol

class Packet:
    # packet header
    HEADER_FORMAT = ">BBBH"
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

    # formats
    CONTROL_FORMAT = HEADER_FORMAT + "Bbbbbbbbb"
    HEARTBEAT_FORMAT = HEADER_FORMAT
    PING_FORMAT = HEADER_FORMAT
    DISCOVERY_REQUEST_FORMAT = HEADER_FORMAT
    # TODO: telemetry format
    DISCOVERY_REPLY_FORMAT = HEADER_FORMAT + "HB"

    @staticmethod
    def encodeHeader(packetType: int, flags: int, sequence: int) -> bytes:
        return struct.pack(
            Packet.HEADER_FORMAT,
            protocol.PROTOCOL_VERSION,
            packetType,
            flags,
            sequence
        )

    @staticmethod
    def decodeHeader(data: bytes):
        if len(data) < Packet.HEADER_SIZE:
            raise ValueError("Packet too small")

        version, packetType, flags, sequence = struct.unpack(
            Packet.HEADER_FORMAT,
            data[:Packet.HEADER_SIZE]
        )

        if version != protocol.PROTOCOL_VERSION:
            raise ValueError("Unsupported protocol version")

        return {
            "version": version,
            "type": packetType,
            "flags": flags,
            "sequence": sequence
        }

    @staticmethod
    def encodeControl(
        flags: int,
        sequence: int,
        driveMode: int,
        throttle: int,
        steering: int,
        left: int,
        right: int,
        lf: int,
        rf: int,
        lr: int,
        rr: int
    ) -> bytes:
        return struct.pack(
            Packet.CONTROL_FORMAT,
            protocol.PROTOCOL_VERSION,
            protocol.PACKET_CONTROL,
            flags,
            sequence,
            driveMode,
            throttle,
            steering,
            left,
            right,
            lf,
            rf,
            lr,
            rr
        )

    @staticmethod
    def decodeControl(data: bytes):
        values = struct.unpack(Packet.CONTROL_FORMAT, data)

        return {
            "version": values[0],
            "type": values[1],
            "flags": values[2],
            "sequence": values[3],

            "driveMode": values[4],

            "throttle": values[5],
            "steering": values[6],

            "left": values[7],
            "right": values[8],

            "lf": values[9],
            "rf": values[10],
            "lr": values[11],
            "rr": values[12]
        }

    @staticmethod
    def encodeHeartbeat(flags: int, sequence: int) -> bytes:
        return Packet.encodeHeader(
            protocol.PACKET_HEARTBEAT,
            flags,
            sequence
        )

    @staticmethod
    def encodePing(flags: int, sequence: int) -> bytes:
        return Packet.encodeHeader(
            protocol.PACKET_PING,
            flags,
            sequence
        )

    @staticmethod
    def encodeDiscoveryRequest(flags: int, sequence: int) -> bytes:
        return Packet.encodeHeader(
            protocol.PACKET_DISCOVERY_REQUEST,
            flags,
            sequence
        )

    @staticmethod
    def encodeDiscoveryReply(flags: int, sequence: int, robotName: str, port: int) -> bytes:
        name = robotName.encode('utf-8')
        return (struct.pack(
            Packet.DISCOVERY_REPLY_FORMAT,
            protocol.PROTOCOL_VERSION,
            protocol.PACKET_DISCOVERY_REPLY,
            flags,
            sequence,
            port,
            len(name)
        ) + name)

    @staticmethod
    def decodeDiscoveryReply(data: bytes):
        headerSize = struct.calcsize(Packet.DISCOVERY_REPLY_FORMAT)
        if len(data) < headerSize:
            return ValueError("Packet too small")

        values = struct.unpack(
            Packet.DISCOVERY_REPLY_FORMAT,
            data[:headerSize]
        )

        nameLength = values[5]

        if len(data) < headerSize + nameLength:
            raise ValueError("Invalid robot name length")

        robotName = data[headerSize:headerSize + nameLength].decode('utf-8')

        return {
            "version": values[0],
            "type": values[1],
            "flags": values[2],
            "sequence": values[3],
            "port": values[4],
            "name": robotName
        }