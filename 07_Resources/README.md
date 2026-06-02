# 07_Resources

Scripts de sincronización, archivos .blend de prueba y releases.

## Archivos

| Archivo | Función |
|---|---|
| `sync_addon.bat` | Copia el addon a la carpeta de extensiones de Blender |
| `sync_addon.ps1` | Versión PowerShell del script de sync |
| `*.blend` | Archivos de prueba y ejemplos |

## Cómo usar sync_addon.bat

Ejecutar desde la raíz del proyecto después de modificar el addon:

```
07_Resources\sync_addon.bat
```

El script copia `02_Blender_Extension/` a la carpeta de extensiones de Blender
configurada en la primera línea del script.
