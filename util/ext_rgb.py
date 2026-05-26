from machine import Pin, PWM

leds = {}

def initLED(name: str, pinR: int, pinG: int, pinB: int):
    if name in leds:
        print(f"LED '{name}' already initialized")
        return False

    r_pwm = PWM(Pin(pinR))
    g_pwm = PWM(Pin(pinG))
    b_pwm = PWM(Pin(pinB))

    for pwm in [r_pwm, g_pwm, b_pwm]:
        pwm.freq(1000)

    leds[name] = {
        'r': r_pwm,
        'g': g_pwm,
        'b': b_pwm
    }

    return True

def setLED(name: str, r: float, g: float, b: float, a=1.0):
    # a = brightness
    if name not in leds:
        print(f"LED '{name}' not initialized")
        return False

    brightness = max(0.0, min(1.0, a))
    led = leds[name]

    led['r'].duty_u16(int(r * 257 * brightness))
    led['g'].duty_u16(int(g * 257 * brightness))
    led['b'].duty_u16(int(b * 257 * brightness))

    return True

def turnOffLED(name: str):
    setLED(name, 0, 0, 0, 0)



