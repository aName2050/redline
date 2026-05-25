import neopixel
import machine

PIN = 22
NUMPIXELS = 2

pixels = neopixel.NeoPixel(machine.Pin(PIN), NUMPIXELS)

def setNEO_LED(led, r, g, b, a=1.0):
    brightness = max(0.0, min(a, 1.0))

    r = int(r * brightness)
    g = int(g * brightness)
    b = int(b * brightness)

    pixels[led] = (r, g, b)
    pixels.write()

