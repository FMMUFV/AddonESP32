@echo off
set /p "=Subiendo proyecto " <nul
for %%f in (*.py *.html) do (
    set /p "=." <nul
    mpremote connect COM6 cp "%%f" :"%%f" > nul 2>&1
)
echo  OK
mpremote connect COM6 exec "from machine import Pin; from time import sleep; led=Pin(2,Pin.OUT); [led.value(i%%2) or sleep(0.15) for i in range(6)]; led.off()" > nul 2>&1
echo Reiniciando placa...
mpremote connect COM6 reset > nul 2>&1
echo Listo!
