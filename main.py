from machine import Pin
from util import pixel

pico_led = Pin("LED", Pin.OUT)
pico_led.on()

pixel.setNEO_LED(0, 0, 255, 0)