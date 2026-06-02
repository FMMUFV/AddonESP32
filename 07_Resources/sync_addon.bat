@echo off
net session >nul 2>&1
if %errorLevel% == 0 (
    powershell -ExecutionPolicy Bypass -File "%~dp0sync_addon.ps1"
) else (
    powershell -Command "Start-Process cmd -ArgumentList '/c powershell -ExecutionPolicy Bypass -File \"%~dp0sync_addon.ps1\"' -Verb RunAs"
)
