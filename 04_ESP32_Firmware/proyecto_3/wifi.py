import network
import socket
from time import sleep_ms, ticks_ms, ticks_diff

_sta = network.WLAN(network.WLAN.IF_STA)
_ap  = network.WLAN(network.WLAN.IF_AP)
_srv = None
_dns = None
_habia_movil = False
_portal_redes = ""

_mdns_sock     = None
_mdns_hostname = 'esp32'
_mdns_ip       = None
_mdns_t        = 0

_web = None

NADA               = 0
MOVIL_CONECTADO    = 1
MOVIL_DESCONECTADO = 2
CREDENCIALES_OK    = 3

# ── mDNS ──────────────────────────────────────────────────────────────────────

def _aton(addr):
    return bytes(int(x) for x in addr.split('.'))

def _mdns_paquete(hostname, my_ip):
    h = hostname.lower()
    label = bytes([len(h)]) + h.encode() + b'\x05local\x00'
    return (
        b'\x00\x00\x84\x00'
        + b'\x00\x00\x00\x01'
        + b'\x00\x00\x00\x00'
        + label
        + b'\x00\x01'
        + b'\x80\x01'
        + b'\x00\x00\x00\x78'
        + b'\x00\x04' + _aton(my_ip)
    )

def _iniciar_mdns(hostname, my_ip):
    global _mdns_sock, _mdns_hostname, _mdns_ip, _mdns_t
    _detener_mdns()
    _mdns_hostname = hostname.lower()
    _mdns_ip = my_ip
    _mdns_t = 0
    sleep_ms(200)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.settimeout(0)
        s.bind(('', 5353))
        try:
            s.setsockopt(0, 3, _aton('224.0.0.251') + _aton(my_ip))
        except:
            pass
        _mdns_sock = s
        try:
            s.sendto(_mdns_paquete(_mdns_hostname, _mdns_ip), ('224.0.0.251', 5353))
        except:
            pass
    except:
        _mdns_sock = None

def _detener_mdns():
    global _mdns_sock, _mdns_ip
    if _mdns_sock:
        try: _mdns_sock.close()
        except: pass
        _mdns_sock = None
    _mdns_ip = None

def tick_mdns():
    global _mdns_t
    if not _mdns_ip:
        return
    now = ticks_ms()
    if not _mdns_sock:
        if ticks_diff(now, _mdns_t) > 1000:
            _mdns_t = now
            _iniciar_mdns(_mdns_hostname, _mdns_ip)
        return
    if ticks_diff(now, _mdns_t) > 3000:
        _mdns_t = now
        try:
            _mdns_sock.sendto(_mdns_paquete(_mdns_hostname, _mdns_ip),
                              ('224.0.0.251', 5353))
        except:
            pass
    try:
        data, addr = _mdns_sock.recvfrom(512)
        if not ((data[2] >> 7) & 1):
            h = _mdns_hostname
            label = bytes([len(h)]) + h.encode() + b'\x05local\x00'
            if label in data:
                pkt = _mdns_paquete(h, _mdns_ip)
                try: _mdns_sock.sendto(pkt, addr)
                except: pass
                try: _mdns_sock.sendto(pkt, ('224.0.0.251', 5353))
                except: pass
    except OSError:
        pass

# ── WiFi ──────────────────────────────────────────────────────────────────────

def conectar(ssid, password, hostname='esp32', intentos=10):
    try:
        network.hostname(hostname)
    except:
        pass
    _sta.active(True)
    if _sta.isconnected():
        _iniciar_mdns(hostname, ip())
        return True
    _sta.connect(ssid, password)
    for _ in range(intentos):
        if _sta.isconnected():
            _iniciar_mdns(hostname, ip())
            return True
        sleep_ms(1000)
    return False

def desconectar():
    _detener_mdns()
    try: _sta.disconnect()
    except: pass
    try: _sta.active(False)
    except: pass

def ip():
    return _sta.ifconfig()[0] if _sta.isconnected() else None

def guardar(ssid, pwd, hostname='esp32'):
    with open('wifi.cfg', 'w') as f:
        f.write(ssid + '\n' + pwd + '\n' + hostname)
    import uos
    uos.sync()

def cargar():
    try:
        with open('wifi.cfg') as f:
            d = f.read().split('\n')
            hostname = d[2].strip() if len(d) >= 3 and d[2].strip() else 'esp32'
            return d[0], d[1], hostname
    except:
        return None

def borrar():
    try:
        import os
        os.remove('wifi.cfg')
    except:
        pass

# ── Servidor de estado ────────────────────────────────────────────────────────

def _html_estado():
    creds = cargar()
    ssid  = creds[0] if creds else '---'
    my_ip = ip() or '---'
    host  = (_mdns_hostname + '.local') if _mdns_sock else '---'
    return (
        "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        "<!DOCTYPE html><html><head>"
        "<meta charset='UTF-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<style>"
        "body{font-family:sans-serif;max-width:380px;margin:30px auto;padding:0 15px}"
        "h2{text-align:center;color:#333;margin-bottom:20px}"
        ".card{background:#f8f9fa;border-radius:10px;padding:16px 20px;margin:12px 0;"
        "border-left:4px solid #1a73e8}"
        ".lbl{font-size:11px;color:#888;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px}"
        ".val{font-size:20px;font-weight:bold;color:#1a73e8}"
        "</style></head><body>"
        "<h2>Estado del dispositivo</h2>"
        "<div class='card'><div class='lbl'>Red WiFi</div>"
        "<div class='val'>" + ssid + "</div></div>"
        "<div class='card'><div class='lbl'>IP</div>"
        "<div class='val'>" + my_ip + "</div></div>"
        "<div class='card'><div class='lbl'>Nombre local</div>"
        "<div class='val'>" + host + "</div></div>"
        "</body></html>"
    )

def iniciar_web():
    global _web
    detener_web()
    try:
        _web = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _web.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        _web.settimeout(0)
        _web.bind(('', 80))
        _web.listen(2)
    except:
        _web = None

def detener_web():
    global _web
    if _web:
        try: _web.close()
        except: pass
        _web = None

def tick_web():
    if _web is None:
        return
    try:
        conn, _ = _web.accept()
        conn.settimeout(1)
        try:
            while True:
                chunk = conn.recv(256)
                if not chunk or len(chunk) < 256:
                    break
        except:
            pass
        conn.send(_html_estado())
        conn.close()
    except OSError:
        pass

# ── Portal cautivo ─────────────────────────────────────────────────────────────

def _dns_respuesta(data):
    return (data[:2] + b'\x81\x80' + data[4:6] +
            b'\x00\x01\x00\x00\x00\x00' + data[12:] +
            b'\xc0\x0c\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04\xc0\xa8\x04\x01')

def iniciar_portal(ap_ssid="ESP32_Config", ap_pwd="12345678"):
    global _srv, _dns, _habia_movil, _portal_redes
    _habia_movil = False
    _sta.active(True)
    _ap.active(True)
    sleep_ms(1500)
    _ap.config(essid=ap_ssid, password=ap_pwd, authmode=3)
    sleep_ms(500)
    _portal_redes = _escanear_redes()

    _srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    _srv.settimeout(0)
    _srv.bind(('', 80))
    _srv.listen(3)

    _dns = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    _dns.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    _dns.settimeout(0)
    _dns.bind(('', 53))

def detener_portal():
    global _srv, _dns, _habia_movil
    for sock in (_srv, _dns):
        if sock:
            try:
                sock.close()
            except:
                pass
    _srv = None
    _dns = None
    _ap.active(False)
    _habia_movil = False

def _moviles():
    try:
        return len(_ap.status('stations')) > 0
    except:
        return False

def _decode(s):
    s = s.replace('+', ' ')
    out = []
    i = 0
    while i < len(s):
        if s[i] == '%' and i + 2 < len(s):
            out.append(chr(int(s[i+1:i+3], 16)))
            i += 3
        else:
            out.append(s[i])
            i += 1
    return ''.join(out)

def _html_ok(hostname, my_ip):
    h = hostname + '.local'
    return (
        "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        "<!DOCTYPE html><html><head>"
        "<meta charset='UTF-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<style>"
        "body{font-family:sans-serif;text-align:center;padding:30px 15px;max-width:400px;margin:0 auto}"
        "h2{color:#34a853;margin-bottom:4px}"
        ".note{color:#888;font-size:0.85em;margin:0 0 18px}"
        ".card{background:#f8f9fa;border-radius:10px;padding:14px 18px;margin:10px 0;"
        "text-align:left;border-left:4px solid #34a853}"
        ".lbl{font-size:11px;color:#888;text-transform:uppercase;letter-spacing:1px}"
        ".row{display:flex;align-items:center;justify-content:space-between;margin-top:4px}"
        ".val{font-size:17px;font-weight:bold;color:#1a73e8}"
        ".btn{padding:7px 14px;background:#e8f0fe;color:#1a73e8;border:none;"
        "border-radius:6px;font-size:13px;cursor:pointer}"
        ".ok{background:#c8e6c9!important;color:#2e7d32!important}"
        "</style></head><body>"
        "<h2>&#10003; Conectado</h2>"
        "<p class='note'>Aplicando cambios en <span id='c'>3</span>s...</p>"
        "<div class='card'><div class='lbl'>Nombre local</div>"
        "<div class='row'><span class='val'>" + h + "</span>"
        "<button class='btn' onclick='cpy(\"" + h + "\",this)'>Copiar</button></div></div>"
        "<div class='card'><div class='lbl'>IP</div>"
        "<div class='row'><span class='val'>" + my_ip + "</span>"
        "<button class='btn' onclick='cpy(\"" + my_ip + "\",this)'>Copiar</button></div></div>"
        "<script>"
        "var n=3;"
        "var t=setInterval(function(){"
        "n--;document.getElementById('c').textContent=n;"
        "if(n<=0){clearInterval(t);document.body.innerHTML='<p style=\"font-family:sans-serif;text-align:center;padding:40px\">Dispositivo reiniciando...</p>';}},1000);"
        "function cpy(t,b){"
        "var i=document.createElement('input');i.value=t;"
        "document.body.appendChild(i);i.select();i.setSelectionRange(0,99);"
        "document.execCommand('copy');document.body.removeChild(i);"
        "b.textContent='Copiado!';b.className='btn ok';"
        "setTimeout(function(){b.textContent='Copiar';b.className='btn'},2000)}"
        "</script>"
        "</body></html>"
    )

def _html_error(ssid):
    return (
        "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        "<!DOCTYPE html><html><head>"
        "<meta charset='UTF-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<style>body{font-family:sans-serif;text-align:center;padding:40px 15px;"
        "max-width:400px;margin:0 auto}"
        ".box{background:#fce8e6;border-radius:10px;padding:20px;margin:20px 0;"
        "border-left:4px solid #ea4335}"
        ".btn{display:inline-block;margin-top:20px;padding:12px 28px;"
        "background:#1a73e8;color:white;border-radius:8px;text-decoration:none;"
        "font-size:15px}"
        "</style></head><body>"
        "<h2 style='color:#ea4335'>No se pudo conectar</h2>"
        "<div class='box'>"
        "<p style='margin:0'>Red: <b>" + ssid + "</b></p>"
        "<p style='margin:8px 0 0;color:#555;font-size:0.9em'>Comprueba que la contrasena es correcta</p>"
        "</div>"
        "<a class='btn' href='http://192.168.4.1/'>Volver a intentarlo</a>"
        "</body></html>"
    )

def _escanear_redes():
    try:
        redes = _sta.scan()
        vistas = set()
        opciones = ""
        for r in sorted(redes, key=lambda x: -x[3]):
            ssid = r[0].decode('utf-8', 'ignore').strip()
            if ssid and ssid not in vistas:
                vistas.add(ssid)
                opciones += "<li onclick='sel(this)'>{}</li>".format(ssid)
        return opciones or "<li>No se encontraron redes</li>"
    except:
        return "<li>Error al escanear</li>"

def _html_portal():
    with open('WifiHtml.html') as f:
        html = f.read().replace('{redes}', _portal_redes)
    return "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nCache-Control: max-age=300\r\n\r\n" + html

def tick():
    global _habia_movil

    if _dns:
        try:
            data, addr = _dns.recvfrom(512)
            _dns.sendto(_dns_respuesta(data), addr)
        except OSError:
            pass

    if _srv is None:
        return NADA

    movil_ahora = _moviles()
    resultado = NADA
    if movil_ahora and not _habia_movil:
        resultado = MOVIL_CONECTADO
    elif not movil_ahora and _habia_movil:
        resultado = MOVIL_DESCONECTADO
    _habia_movil = movil_ahora

    try:
        conn, _ = _srv.accept()
        conn.settimeout(1)
        req = b''
        try:
            while True:
                chunk = conn.recv(256)
                if not chunk:
                    break
                req += chunk
                if len(chunk) < 256:
                    break
        except:
            pass
        req = req.decode('utf-8', 'ignore')

        if 'POST' in req and 's=' in req:
            body = req.split('\r\n\r\n', 1)[-1]
            params = {}
            for par in body.split('&'):
                if '=' in par:
                    k, v = par.split('=', 1)
                    params[k] = _decode(v)
            ssid     = params.get('s', '').strip()
            pwd      = params.get('p', '').strip()
            hostname = params.get('h', '').strip() or 'esp32'
            _sta.active(True)
            _sta.connect(ssid, pwd)
            my_ip = None
            for _ in range(10):
                sleep_ms(500)
                if _sta.isconnected():
                    my_ip = ip()
                    break
            if my_ip:
                guardar(ssid, pwd, hostname)
                conn.send(_html_ok(hostname, my_ip))
                conn.close()
                from machine import Pin, reset
                led = Pin(2, Pin.OUT)
                for _ in range(30):
                    led.value(not led.value())
                    sleep_ms(100)
                reset()
            else:
                try: _sta.disconnect()
                except: pass
                conn.send(_html_error(ssid))
                conn.close()
        else:
            conn.send(_html_portal())
            conn.close()
    except OSError:
        pass

    return resultado
