# sync_addon.ps1 — Copia archivos fuente a la carpeta instalada de Blender

$src = "C:\Users\Usuario\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Blender\Seleccion_Addon\AddonESP32\02_Blender_Extension"
$dst = "C:\Users\Usuario\AppData\Roaming\Blender Foundation\Blender\5.0\extensions\user_default\addon_esp32"

Write-Host ""
Write-Host "=== AddonESP32 — Sync Addon ===" -ForegroundColor Cyan

Write-Host "Copiando addon a Blender..." -ForegroundColor Gray
if (-not (Test-Path $dst)) { New-Item -ItemType Directory -Force -Path $dst | Out-Null }
Copy-Item -Recurse -Force "$src\*" "$dst\"

Write-Host "[OK] Sincronizado." -ForegroundColor Green

$manifest = Join-Path $dst "blender_manifest.toml"
$ver = Select-String -Path $manifest -Pattern '^version' | Select-Object -First 1
Write-Host "Version instalada: $($ver.Line)" -ForegroundColor White
Write-Host ""
Write-Host "Reinicia Blender o pulsa 'Refrescar Addon' en el N-Panel." -ForegroundColor Cyan
Write-Host ""
Start-Sleep -Seconds 2
