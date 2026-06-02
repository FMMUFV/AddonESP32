# Especificaciones del Proyecto 2 — ESP32 WiFi

## 1. Hardware

### Placa Principal
| Componente | Detalle |
|---|---|
| Modelo | ESP32 NodeMCU (30 pines) |
| Chip de comunicación | CH340C |

### Placa de Expansión (Base Breakout)
| Característica | Detalle |
|---|---|
| Entrada Jack | 6.5 V – 16 V |
| Entrada USB-C | 5 V |
| Entrada Micro-USB | 5 V |
| Selector de voltaje (JUMP) | Conmuta entre **3.3 V** y **5 V** en los pines laterales |

---

## 2. Firmware

| Firmware | Versión | Fecha |
|---|---|---|
| MicroPython ESP32_GENERIC | v1.28.0 | 2026-04-06 |

> Flasheado con `esptool v5.2.0` a 115200 baudios en dirección `0x1000`.

---

## 3. Archivos del proyecto

| Archivo | Función |
|---|---|
| `main.py` | Punto de entrada, máquina de estados WiFi |
| `wifi.py` | Portal cautivo, conexión WiFi, guardado de credenciales |
| `BotonBoot.py` | Control del LED y botón BOOT |
| `WifiHtml.html` | Página web de configuración WiFi |
| `boot.py` | Arranque previo al main |
| `upload.bat` | Subida de archivos a la ESP32 |

---

## 4. Comportamiento del LED y botón BOOT

| LED | Estado |
|---|---|
| Parpadeo lento (1s) | Portal WiFi activo — esperando configuración |
| Encendido fijo | Conectado a WiFi |

| Acción BOOT | Resultado |
|---|---|
| Pulsación corta (conectado) | Borra credenciales y reinicia el portal |

---

## 5. Flujo WiFi

```
Arranque
    │
    ▼
Portal activo (LED parpadeo lento)
    │
    │  Móvil conecta a ESP32_Config
    ▼
Página web → usuario elige red y contraseña
    │
    │  Credenciales recibidas
    ▼
ESP32 conecta a WiFi de casa (LED encendido fijo)
    │
    │  Pulsar BOOT
    ▼
Borra credenciales → vuelve al portal
```

---

## 6. Herramientas de subida

### mpremote + upload.bat
- Desconectar Pymakr → ejecutar `.\upload.bat` desde la carpeta `proyecto_2`
- Sube todos los `.py` y `.html`, parpadea el LED 3 veces y reinicia la placa
