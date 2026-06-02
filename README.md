# AddonESP32 — Blender + ESP32

Addon de Blender que integra placas **ESP32** con el entorno 3D.
Combina Python en Blender, Geometry Nodes y MicroPython en la placa para crear
un puente de datos bidireccional entre el mundo físico (sensores, actuadores)
y el mundo virtual (visualización, automatización).

**Repositorio:** https://github.com/FMMUFV/AddonESP32.git  
**Versión actual:** 0.1.0  
**Hardware:** ESP32 NodeMCU (30 pines, CH340C) + MicroPython v1.28.0  
**Blender mínimo:** 4.5.2 LTS  

---

## Estructura de Directorios

| Carpeta | Contenido |
|---|---|
| `01_Architecture_Docs/` | CLAUDE.md, roadmap, registro de decisiones |
| `02_Blender_Extension/` | Addon instalable para Blender |
| `03_Geometry_Nodes/` | Módulos de Geometry Nodes para visualización |
| `04_ESP32_Firmware/` | MicroPython: firmware y proyectos para la placa |
| `05_ESP32_Blender_Bridge/` | Puente de comunicación ESP32 ↔ Blender |
| `06_QA_and_Watchdog/` | Tests, benchmarks y compatibilidad |
| `07_Resources/` | Scripts de sync, archivos .blend, releases |
| `08_Web_Preview/` | Interfaz web embebida en la ESP32 |

---

## Flujo de Desarrollo

```
Editar addon en 02_Blender_Extension/
        ↓
Ejecutar 07_Resources/sync_addon.bat
        ↓
Pulsar "Refrescar Addon" en N-Panel  (cambios de lógica)
    — o —
Reiniciar Blender                    (cambios estructurales)

Editar firmware en 04_ESP32_Firmware/
        ↓
Ejecutar upload.bat desde la carpeta del proyecto
        ↓
Verificar parpadeo LED × 3 (confirmación de subida)
```

---

## Convenciones Git

- Commits semánticos: `feat(addon):`, `feat(esp32):`, `fix(bridge):`, `docs:`, `chore:`
- Tags: `v0.x.x`
- Rama principal: `main`
