import BotonBoot as bb_mod
import wifi
from time import sleep_ms

bb = bb_mod.BotonBoot()

DESCONECTADO = 0
BUSCANDO     = 1
CONECTADO    = 2

_creds_prev = None

def _intentar_conectar(creds):
    if not creds:
        bb.set_modo(bb_mod.APAGADO)
        return DESCONECTADO
    hostname = creds[2] if len(creds) > 2 else 'esp32'
    if wifi.conectar(creds[0], creds[1], hostname):
        bb.set_modo(bb_mod.ENCENDIDO)
        return CONECTADO
    bb.set_modo(bb_mod.APAGADO)
    return DESCONECTADO

# Arranque: conectar y arrancar servidor de estado si hay credenciales
estado = _intentar_conectar(wifi.cargar())
if estado == CONECTADO:
    wifi.iniciar_web()

while True:
    bb.actualizar()
    wifi.tick_mdns()
    wifi.tick_web()

    if bb.pulsado():
        if estado == BUSCANDO:
            # Cancelar: volver al estado anterior
            wifi.detener_portal()
            wifi.desconectar()
            estado = _intentar_conectar(_creds_prev)
            if estado == CONECTADO:
                wifi.iniciar_web()
            _creds_prev = None
        else:
            # Iniciar portal para cambiar de WiFi
            wifi.detener_web()
            _creds_prev = wifi.cargar()
            wifi.desconectar()
            wifi.iniciar_portal()
            bb.set_modo(bb_mod.PARPADEO_LENTO)
            estado = BUSCANDO

    elif estado == BUSCANDO:
        r = wifi.tick()
        if r == wifi.CREDENCIALES_OK:
            wifi.detener_portal()
            wifi.desconectar()
            estado = _intentar_conectar(wifi.cargar())
            if estado == DESCONECTADO and _creds_prev:
                wifi.guardar(_creds_prev[0], _creds_prev[1], _creds_prev[2] if len(_creds_prev) > 2 else 'esp32')
                estado = _intentar_conectar(_creds_prev)
            if estado == CONECTADO:
                wifi.iniciar_web()
            _creds_prev = None

    sleep_ms(10)
