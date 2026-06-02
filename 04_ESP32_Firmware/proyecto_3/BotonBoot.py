from machine import Pin
from time import ticks_ms

APAGADO         = 0
ENCENDIDO       = 1
PARPADEO_LENTO  = 2   # 1000ms - WiFi
PARPADEO_RAPIDO = 3   # 150ms  - Bluetooth

class BotonBoot:
    def __init__(self):
        self._led = Pin(2, Pin.OUT)
        self._btn = Pin(15, Pin.IN, Pin.PULL_UP)
        self._modo = APAGADO
        self._led_val = False
        self._last_toggle = 0
        self._last_press = 0
        self._led.off()

    def set_modo(self, modo):
        self._modo = modo
        self._last_toggle = ticks_ms()
        if modo == APAGADO:
            self._led.off()
            self._led_val = False
        elif modo == ENCENDIDO:
            self._led.on()
            self._led_val = True
        else:
            self._led.on()
            self._led_val = True

    def actualizar(self):
        now = ticks_ms()
        if self._modo == PARPADEO_LENTO and now - self._last_toggle >= 1000:
            self._led_val = not self._led_val
            self._led.value(self._led_val)
            self._last_toggle = now
        elif self._modo == PARPADEO_RAPIDO and now - self._last_toggle >= 150:
            self._led_val = not self._led_val
            self._led.value(self._led_val)
            self._last_toggle = now

    def pulsado(self):
        now = ticks_ms()
        if self._btn.value() == 0 and now - self._last_press > 300:
            self._last_press = now
            return True
        return False
