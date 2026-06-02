# Constructor_Sistema.md
## Guía de Arquitectura — AddonESP32

> Documento de referencia para diseñar y ampliar el sistema.
> Inspirado en la metodología del proyecto FaceSet Retopology FMM (FASET).

---

## 1. Principios del Sistema

### 1.1 Separación de responsabilidades

Cada capa del sistema tiene su propia carpeta y no invade la de las demás:

```
02_Blender_Extension/    ← Todo lo que vive en Blender (UI, operadores)
03_Geometry_Nodes/       ← Nodos GN (visualización de datos)
04_ESP32_Firmware/       ← Todo lo que corre en la placa (MicroPython)
05_ESP32_Blender_Bridge/ ← Protocolo de comunicación entre ambos mundos
```

### 1.2 La placa no depende de Blender

La ESP32 funciona de forma autónoma. Blender es un **cliente opcional**
que se conecta a ella, no un requisito para que la placa opere.

### 1.3 El bridge es el único que conoce los dos mundos

`05_ESP32_Blender_Bridge/` es la única capa que habla tanto Python de Blender
como el protocolo HTTP de la ESP32. El addon no hace peticiones de red directamente;
las delega al módulo bridge.

---

## 2. Mapa del Sistema

```
┌─────────────────────────────────────────────────────┐
│                    BLENDER                          │
│                                                     │
│  N-Panel (panels.py)                                │
│      │                                              │
│      ▼                                              │
│  Operadores (operators.py)                          │
│      │                                              │
│      ▼                                              │
│  Bridge (bridge.py) ◄─── 05_ESP32_Blender_Bridge/  │
│      │                                              │
│      │  HTTP REST / WebSocket                       │
└──────┼──────────────────────────────────────────────┘
       │
       │  WiFi (red local)
       │
┌──────┼──────────────────────────────────────────────┐
│      ▼                                              │
│  Servidor HTTP (server.py)   ESP32                  │
│      │                                              │
│      ▼                                              │
│  Lógica principal (main.py)                         │
│      │                                              │
│      ├── wifi.py       (conexión WiFi)              │
│      ├── BotonBoot.py  (LED + botón)                │
│      └── [sensores / actuadores futuros]            │
└─────────────────────────────────────────────────────┘
```

---

## 3. Cómo añadir un nuevo proyecto ESP32

### Paso 1 — Crear la carpeta del proyecto

```
04_ESP32_Firmware/
└── proyecto_N/
    ├── PROYECTO.md       ← Estado, tareas, historial
    ├── ESPECIFICACIONES.md
    ├── main.py
    ├── boot.py
    ├── wifi.py
    ├── server.py
    ├── BotonBoot.py
    ├── WifiHtml.html
    └── upload.bat
```

### Paso 2 — Rellenar ESPECIFICACIONES.md

Usar la plantilla de la sección 5. Documentar el hardware exacto,
el firmware, el flujo WiFi y los endpoints del servidor.

### Paso 3 — Definir los endpoints REST

Cada proyecto expone una API REST mínima en `server.py`.
Documentar en ESPECIFICACIONES.md:

| Endpoint | Método | Descripción |
|---|---|---|
| `/ping` | GET | Responde `{"status": "ok"}` |
| `/data` | GET | Devuelve datos de sensores |
| `/set` | POST | Recibe comandos de Blender |

### Paso 4 — Subir a la placa

```
1. Desconectar Pymakr en VS Code
2. cd 04_ESP32_Firmware\proyecto_N
3. .\upload.bat
4. Esperar × 3 parpadeos del LED
```

---

## 4. Cómo añadir un nuevo operador al addon

### Archivos a modificar

| Archivo | Cambio |
|---|---|
| `operators.py` | Añadir clase `ADDESP32_OT_<nombre>` |
| `panels.py` | Añadir botón en la sección correspondiente |
| `bridge.py` | Añadir función de comunicación si necesita red |
| `__init__.py` | Registrar la nueva clase |

### Plantilla del operador

```
ADDESP32_OT_<nombre>
    bl_idname  = "addesp32.<nombre>"
    bl_label   = "<Etiqueta visible en el panel>"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        # Condición para que el botón esté activo

    def execute(self, context):
        # Lógica del operador
        # Llamar a bridge.<funcion>() si necesita red
        return {"FINISHED"}
```

---

## 5. Plantilla ESPECIFICACIONES.md (para cada proyecto ESP32)

```markdown
# Especificaciones — Proyecto N: <Nombre>

## 1. Hardware
| Componente | Detalle |
|---|---|
| Modelo | ESP32 NodeMCU (30 pines) |
| Chip | CH340C |

## 2. Firmware
| Firmware | Versión |
|---|---|
| MicroPython ESP32_GENERIC | v1.28.0 |

## 3. Archivos del proyecto
| Archivo | Función |
|---|---|
| `main.py` | ... |
| `server.py` | ... |

## 4. Endpoints REST
| Endpoint | Método | Descripción |
|---|---|---|
| `/ping` | GET | ... |

## 5. Flujo principal
[diagrama de flujo]

## 6. Herramientas de subida
mpremote + upload.bat — ver sección 3.4 del Constructor_Sistema.md
```

---

## 6. Convenciones de Nombres

| Elemento | Convención | Ejemplo |
|---|---|---|
| Clases addon | `ADDESP32_OT_<nombre>` | `ADDESP32_OT_ping` |
| Panel addon | `ADDESP32_PT_<nombre>` | `ADDESP32_PT_main` |
| Preferencias | `ADDESP32_Preferences` | — |
| Proyectos ESP32 | `proyecto_N` | `proyecto_4` |
| Endpoints REST | lowercase con `_` | `/get_sensor_data` |

---

## 7. Checklist para una nueva funcionalidad completa

- [ ] Definir el endpoint REST en `04_ESP32_Firmware/proyecto_N/server.py`
- [ ] Documentar endpoint en `ESPECIFICACIONES.md` del proyecto
- [ ] Implementar la función en `05_ESP32_Blender_Bridge/bridge.py`
- [ ] Crear operador en `02_Blender_Extension/operators.py`
- [ ] Añadir botón en `02_Blender_Extension/panels.py`
- [ ] Subir versión en `blender_manifest.toml` y `__init__.py`
- [ ] Subir firmware a la placa con `upload.bat`
- [ ] Commit con prefijo semántico: `feat(bridge):` o `feat(addon):`
