# 04_ESP32_Firmware

Proyectos MicroPython para la placa ESP32.
Cada subcarpeta es un proyecto independiente y autónomo.

## Estructura de cada proyecto

```
proyecto_N/
├── PROYECTO.md          ← Estado actual, tareas e historial
├── ESPECIFICACIONES.md  ← Hardware, firmware, flujos, endpoints
├── main.py              ← Punto de entrada
├── boot.py              ← Arranque previo al main
├── wifi.py              ← Conexión WiFi y portal cautivo
├── server.py            ← Servidor HTTP con endpoints REST
├── BotonBoot.py         ← Control LED y botón BOOT
├── WifiHtml.html        ← Página web de configuración WiFi
└── upload.bat           ← Subida a la placa via mpremote
```

## Hardware base

- ESP32 NodeMCU (30 pines, CH340C)
- Driver: CH341SER.EXE → puerto COM en Windows
- Firmware: MicroPython v1.28.0

## Cómo subir código a la placa

```
1. Desconectar Pymakr en VS Code
2. cd 04_ESP32_Firmware\proyecto_N
3. .\upload.bat
4. LED parpadea × 3 → subida correcta → placa reinicia
```

## Herramientas necesarias

- `mpremote` — `pip install mpremote`
- Pymakr (VS Code) — solo para REPL / consola

## Proyectos

| Carpeta | Descripción | Estado |
|---|---|---|
| `proyecto_1/` | — | — |
| `proyecto_2/` | — | — |
| `proyecto_3/` | — | — |
