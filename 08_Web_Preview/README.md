# 08_Web_Preview

Interfaz web embebida en la ESP32 y preview de la misma en el navegador.

## Contenido

| Archivo | Función |
|---|---|
| `index.html` | Página principal de la interfaz web de la ESP32 |
| `wifi_setup.html` | Página del portal cautivo de configuración WiFi |

## Uso

La ESP32 sirve estos archivos HTML desde su servidor HTTP interno.
Se accede desde cualquier dispositivo conectado a la misma red WiFi:

```
http://<IP_de_la_ESP32>/
```

Durante el desarrollo se puede abrir directamente en el navegador
para previsualizar la UI sin necesidad de la placa.
