# 02_Blender_Extension

Addon instalable para Blender. Contiene el panel de control, los operadores
y la lógica de comunicación con la ESP32 desde dentro de Blender.

## Archivos principales

| Archivo | Función |
|---|---|
| `__init__.py` | Registro del addon, version, handlers |
| `blender_manifest.toml` | Metadatos Extensions API (Blender 4.5+) |
| `panels.py` | N-Panel en el viewport 3D |
| `operators.py` | Operadores: conectar, enviar, recibir |
| `preferences.py` | IP de la ESP32, puerto COM, ajustes |
| `bridge.py` | Módulo de red (HTTP / WebSocket) |

## Cómo instalar en Blender

1. Comprimir esta carpeta como `.zip`
2. Blender → Edit → Preferences → Add-ons → Install from Disk
3. Activar **AddonESP32**

## Cómo sincronizar durante el desarrollo

Ejecutar `07_Resources/sync_addon.bat` después de cada cambio.
Ver flujo completo en `01_Architecture_Docs/CLAUDE.md`.
