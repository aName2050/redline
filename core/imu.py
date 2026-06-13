from machine import I2C, Pin
import struct
import time
import math

class IMU:
    def __init__(self, scl=1, sda=0):
        self.i2c = I2C(0, scl=Pin(scl), sda=Pin(sda), freq=400000)
        self.addr = 0x68

        # wake MPU
        self.i2c.writeto_mem(self.addr, 0x6B, b'\x00')

        # bias
        self.bx = self.by = self.bz = 0

        # orientation
        self.pitch = 0
        self.roll = 0
        self.yaw = 0

        self.last_time = time.ticks_ms()

    def read_raw(self):
        data = self.i2c.readfrom_mem(self.addr, 0x3B, 14)
        vals = struct.unpack(">hhhhhhh", data)

        ax, ay, az = vals[0], vals[1], vals[2]
        gx, gy, gz = vals[4], vals[5], vals[6]

        return (
            ax/16384, ay/16384, az/16384,
            gx/131, gy/131, gz/131
        )

    def calibrate(self, samples=200):
        bx = by = bz = 0

        for _ in range(samples):
            _, _, _, gx, gy, gz = self.read_raw()
            bx += gx; by += gy; bz += gz
            time.sleep_ms(5)

        self.bx = bx / samples
        self.by = by / samples
        self.bz = bz / samples

    def update(self):
        ax, ay, az, gx, gy, gz = self.read_raw()

        # remove bias
        gx -= self.bx
        gy -= self.by
        gz -= self.bz

        # time delta
        now = time.ticks_ms()
        dt = time.ticks_diff(now, self.last_time) / 1000
        self.last_time = now

        # accel angles
        accel_pitch = math.atan2(ax, (ay**2 + az**2)**0.5)
        accel_roll  = math.atan2(ay, (ax**2 + az**2)**0.5)

        # gyro integration
        self.pitch += math.radians(gx) * dt
        self.roll  += math.radians(gy) * dt
        self.yaw   += math.radians(gz) * dt

        # complementary filter
        alpha = 0.98
        self.pitch = alpha*self.pitch + (1-alpha)*accel_pitch
        self.roll  = alpha*self.roll  + (1-alpha)*accel_roll

        print(self.pitch, self.roll, self.yaw)

    def get(self):
        return {
            "pitch": math.degrees(self.pitch),
            "roll": math.degrees(self.roll),
            "yaw": math.degrees(self.yaw)
        }