# 03_Geometry_Nodes

Módulos standalone de Geometry Nodes para visualizar datos recibidos de la ESP32
dentro de Blender.

## Uso

Cada archivo `.py` es un constructor de un NodeGroup de GN.
Se ejecutan desde Blender o se integran en el addon como parte del sistema FMM.

## Convenciones de nombres

| Elemento | Convención | Ejemplo |
|---|---|---|
| Archivo del módulo | `gn_<nombre>.py` | `gn_sensor_data.py` |
| NodeGroup creado | `ESP32_<Nombre>` | `ESP32_SensorData` |

## Relación con el addon

El addon (`02_Blender_Extension/`) puede construir y actualizar estos NodeGroups
automáticamente al recibir datos de la ESP32.
Ver patrón de construcción en `01_Architecture_Docs/Constructor_Sistema.md`.
