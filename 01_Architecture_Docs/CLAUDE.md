# CLAUDE.md — AddonESP32 v0.1.0
## Memoria Maestra del Proyecto

---

## Visión General

Addon de Blender que conecta el entorno 3D con placas **ESP32** vía WiFi.
El addon actúa como panel de control en Blender para enviar y recibir datos
de sensores y actuadores físicos conectados a la placa.

**Repositorio:** https://github.com/FMMUFV/AddonESP32.git  
**Versión actual:** 0.1.0  
**Nombre del addon en Blender:** AddonESP32  

---

## Stack Tecnológico

| Capa | Tecnología | Función |
|---|---|---|
| Blender UI | Python + `bpy` | Panel de control, operadores |
| Visualización | Geometry Nodes | Representación 3D de datos ESP32 |
| Comunicación | Python `socket` / HTTP | Puente Blender ↔ ESP32 |
| Firmware | MicroPython v1.28.0 | Lógica en la placa |
| Hardware | ESP32 NodeMCU (CH340C) | Placa física |

---

## Estructura de Directorios

| Carpeta | Contenido |
|---|---|
| `01_Architecture_Docs/` | CLAUDE.md, roadmap, registro de decisiones |
| `02_Blender_Extension/` | Addon instalable completo |
| `03_Geometry_Nodes/` | Módulos GN standalone (fuente de nodos) |
| `04_ESP32_Firmware/` | MicroPython — proyectos para la placa |
| `05_ESP32_Blender_Bridge/` | Puente de comunicación ESP32 ↔ Blender |
| `06_QA_and_Watchdog/` | QA: tests, compat, benchmarks |
| `07_Resources/` | sync scripts, .blend, zips de distribución |
| `08_Web_Preview/` | Interfaz web embebida (servidor HTTP en ESP32) |

---

## Hardware Conocido

### Placa Principal
| Componente | Detalle |
|---|---|
| Modelo | ESP32 NodeMCU (30 pines) |
| Chip de comunicación | CH340C |
| Driver Windows | CH341SER.EXE (puerto COM asignado automáticamente) |

### Placa de Expansión (Base Breakout)
| Característica | Detalle |
|---|---|
| Entrada Jack | 6.5 V – 16 V |
| Entrada USB-C | 5 V |
| Entrada Micro-USB | 5 V |
| Selector de voltaje (JUMP) | Conmuta entre 3.3 V y 5 V en los pines laterales |

---

## Firmware

| Firmware | Versión | Fecha | Archivo |
|---|---|---|---|
| MicroPython ESP32_GENERIC | v1.28.0 | 2026-04-06 | `ESP32_GENERIC-20260406-v1.28.0.bin` |

> Flasheado con `esptool v5.2.0` a 115200 baudios en dirección `0x1000`.

---

## Flujo de Subida de Firmware (ESP32)

```
Editar .py en 04_ESP32_Firmware/<proyecto>/
        ↓
Desconectar Pymakr (VS Code)
        ↓
Ejecutar .\upload.bat desde la carpeta del proyecto
        ↓
mpremote sube todos los .py vía COM6
        ↓
LED parpadea × 3  →  subida correcta
        ↓
Placa reinicia automáticamente
```

**Herramientas de subida:**
- `mpremote` — transferencia oficial de MicroPython (`pip install mpremote`)
- `upload.bat` — script que automatiza mpremote (en cada carpeta de proyecto)
- Pymakr (VS Code) — solo para REPL / consola (NO para subir archivos)

---

## Flujo de Desarrollo del Addon (Blender)

```
Editar código en 02_Blender_Extension/
        ↓
Ejecutar 07_Resources/sync_addon.bat
        ↓
Pulsar "Refrescar Addon" en N-Panel  (cambios de lógica)
    — o —
Reiniciar Blender                    (cambios estructurales)
```

**Regla de versiones:** cada modificación sube el número en `blender_manifest.toml`
y en `ADDON_VERSION` de `__init__.py`. Ambos deben coincidir siempre.

---

## Sistema de Comunicación ESP32 ↔ Blender

La comunicación entre Blender y la ESP32 se gestiona en `05_ESP32_Blender_Bridge/`.
Los mecanismos disponibles son:

| Mecanismo | Dirección | Descripción |
|---|---|---|
| HTTP GET/POST | Blender → ESP32 | Blender hace peticiones al servidor HTTP de la ESP32 |
| WebSocket | Bidireccional | Canal de datos en tiempo real |
| Serial / COM | Blender → ESP32 | Acceso directo por puerto COM (solo debug) |

La ESP32 expone un servidor HTTP en su IP local (configurada vía portal WiFi).
Blender obtiene la IP desde las preferencias del addon y hace peticiones REST.

---

## Módulos del Addon (02_Blender_Extension/)

| Archivo | Función |
|---|---|
| `__init__.py` | Register/unregister + handler load_post |
| `blender_manifest.toml` | Metadatos, versión, compatibilidad |
| `panels.py` | N-Panel: conexión ESP32, control, visualización |
| `operators.py` | Operadores: conectar, enviar datos, recibir datos |
| `preferences.py` | IP de la ESP32, puerto COM, ajustes de red |
| `bridge.py` | Módulo de comunicación HTTP/WebSocket |

---

## Proyectos ESP32 (04_ESP32_Firmware/)

Cada proyecto es una carpeta independiente con sus propios archivos:

| Archivo | Función |
|---|---|
| `main.py` | Punto de entrada principal |
| `boot.py` | Arranque previo al main |
| `wifi.py` | Conexión WiFi y portal cautivo |
| `server.py` | Servidor HTTP con endpoints REST |
| `BotonBoot.py` | Control LED y botón BOOT |
| `WifiHtml.html` | Página web de configuración WiFi |
| `upload.bat` | Sube todos los .py a la placa |
| `PROYECTO.md` | Estado, tareas e historial del proyecto |
| `ESPECIFICACIONES.md` | Hardware, software y flujos del proyecto |

---

## Compatibilidad

- Extensions API: `blender_manifest.toml` reemplaza `bl_info`
- `blender_version_min = "4.5.2"`
- Imports relativos dentro del addon
- No commitear zips binarios ni archivos .blend1

---

## Convenciones Git

- Commits semánticos: `feat(addon):`, `feat(esp32):`, `fix(bridge):`, `docs:`, `chore:`
- Tags: `v0.x.x`
- Rama principal: `main`

---

## Registro de Decisiones

| Fecha | Decisión | Motivo |
|---|---|---|
| 2026-06-02 | Estructura inicial de carpetas | Separación addon / firmware / bridge |
| 2026-06-02 | MicroPython como firmware ESP32 | Ya probado en proyectos anteriores (v1.28.0) |
| 2026-06-02 | HTTP REST como protocolo base | Simple, sin dependencias externas en ESP32 |
| 2026-06-02 | Carpeta Bridge separada del addon | El protocolo puede cambiar sin tocar el addon |

---

## Roadmap

- [ ] Estructura de carpetas y documentación inicial
- [ ] Addon mínimo: panel con campo IP + botón Ping
- [ ] Servidor HTTP mínimo en ESP32 (endpoint `/ping`)
- [ ] Bridge: Blender hace GET a ESP32 y muestra respuesta
- [ ] Geometry Nodes: visualización de datos recibidos
- [ ] WebSocket para datos en tiempo real
- [ ] Sistema de descubrimiento mDNS de la placa
