# 06_QA_and_Watchdog

Tests, benchmarks y comprobaciones de compatibilidad.

## Archivos

| Archivo | Función |
|---|---|
| `test_runner.py` | Ejecuta todos los tests desde Blender |
| `compatibility.py` | Verifica versión de Blender y dependencias |
| `benchmarks.py` | Mide tiempos de respuesta del bridge |
| `connectivity.py` | Comprueba que la ESP32 responde en la red |

## Cómo ejecutar los tests

Desde el Script Editor de Blender o desde la terminal:

```
blender --background --python 06_QA_and_Watchdog/test_runner.py
```
