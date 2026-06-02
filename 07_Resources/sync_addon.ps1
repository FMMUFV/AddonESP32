$src = "C:\Users\Usuario\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Blender\Seleccion_Addon\AddonESP32\02_Blender_Extension"

$dsts = @(
    "C:\Users\Usuario\AppData\Roaming\Blender Foundation\Blender\5.0\extensions\user_default\addon_esp32",
    "C:\Users\Usuario\AppData\Roaming\Blender Foundation\Blender\5.1\extensions\user_default\addon_esp32"
)

Write-Host "=== ESP32 FMM - Sync Addon ===" -ForegroundColor Cyan

foreach ($dst in $dsts) {
    $ver = Split-Path (Split-Path $dst -Parent) -Parent | Split-Path -Leaf
    Write-Host "Blender $ver ..." -ForegroundColor Gray
    if (-not (Test-Path $dst)) { New-Item -ItemType Directory -Force -Path $dst | Out-Null }
    Copy-Item -Recurse -Force "$src\*" "$dst\"
    Write-Host "  OK" -ForegroundColor Green
}

Write-Host "Listo. Reinicia Blender." -ForegroundColor Cyan
Start-Sleep -Seconds 2
