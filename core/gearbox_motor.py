from machine import Pin, PWM

class GearboxMotor:
    CONTROL_TYPE = {
        'duty_cycle': 0
    }

    def __init__(self, neg_pin: int, pos_pin: int) -> None:
        self.fwd = PWM(Pin(pos_pin))
        self.rev = PWM(Pin(neg_pin))

        self.fwd.freq(1000)
        self.rev.freq(1000)

        self.fwd.duty_u16(0)
        self.rev.duty_u16(0)

        self.inverse = False

        self.current_speed = 0

        self.state = 'stopped'

    def getState(self) -> str:
        return self.state

    def setSpeed(self, speed: float, controlType: int) -> None:
        speed = max(-1.0, min(1.0, speed))
        self.current_speed = speed

        if self.inverse:
            speed = -speed

        if controlType == self.CONTROL_TYPE['duty_cycle']:
            if speed > 0:
                self.fwd.duty_u16(int(speed * 65535))
                self.rev.duty_u16(0)
                self.state = 'forward'
            elif speed < 0:
                self.fwd.duty_u16(0)
                self.rev.duty_u16(int(-speed * 65535))
                self.state = 'reverse'
            else:
                self.fwd.duty_u16(0)
                self.rev.duty_u16(0)
                self.state = 'stopped'

    def getSpeed(self) -> float:
        return self.current_speed

    def stopMotor(self) -> None:
        self.fwd.duty_u16(0)
        self.rev.duty_u16(0)
        self.state = 'stopped'

    def setInverse(self, inverse: bool) -> None:
        self.inverse = inverse
