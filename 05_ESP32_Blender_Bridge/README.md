# 05_ESP32_Blender_Bridge

Capa de comunicación entre Blender y la ESP32.
Es el único módulo del sistema que "habla" con los dos mundos a la vez.

## Responsabilidad

- Enviar comandos desde Blender a la ESP32 (HTTP POST)
- Recibir datos de la ESP32 en Blender (HTTP GET / WebSocket)
- Gestionar la IP de la placa y los timeouts de red
- Traducir entre el formato de datos de la ESP32 (JSON) y los objetos de Blender

## Archivos

| Archivo | Función |
|---|---|
| `bridge.py` | Módulo principal de comunicación |
| `discovery.py` | Descubrimiento de la IP de la placa en la red local |
| `protocol.md` | Especificación del protocolo de datos |

## Protocolo base

La ESP32 expone un servidor HTTP. Blender hace peticiones REST:

```
Blender                          ESP32
   │                               │
   │── GET /ping ─────────────────►│
   │◄─ {"status": "ok"} ──────────│
   │                               │
   │── GET /data ─────────────────►│
   │◄─ {"sensor": 1234} ──────────│
   │                               │
   │── POST /set {"led": true} ───►│
   │◄─ {"ok": true} ──────────────│
```

## Cómo ampliar el protocolo

1. Añadir el endpoint en `04_ESP32_Firmware/proyecto_N/server.py`
2. Documentarlo en `ESPECIFICACIONES.md` del proyecto ESP32
3. Añadir la función correspondiente en `bridge.py`
4. Crear el operador en `02_Blender_Extension/operators.py`

Ver guía completa en `01_Architecture_Docs/Constructor_Sistema.md`.
