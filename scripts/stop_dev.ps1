Write-Host "Stopping OpenMCP Services..."

# Kill Python processes (uvicorn servers)
Write-Host "Stopping Python processes..."
Get-Process | Where-Object { $_.ProcessName -eq "python" -and $_.MainWindowTitle -like "*uvicorn*" } | ForEach-Object {
    Write-Host "Stopping process: $($_.Id) - $($_.MainWindowTitle)"
    Stop-Process -Id $_.Id -Force
}

# Kill Node processes (dashboard)
Write-Host "Stopping Node processes..."
Get-Process | Where-Object { $_.ProcessName -eq "node" -and $_.MainWindowTitle -like "*npm*" } | ForEach-Object {
    Write-Host "Stopping process: $($_.Id) - $($_.MainWindowTitle)"
    Stop-Process -Id $_.Id -Force
}

# Kill any remaining PowerShell windows
Write-Host "Stopping remaining PowerShell windows..."
Get-Process | Where-Object { $_.ProcessName -eq "powershell" -and $_.MainWindowTitle -like "*OpenMCP*" } | ForEach-Object {
    Write-Host "Stopping process: $($_.Id) - $($_.MainWindowTitle)"
    Stop-Process -Id $_.Id -Force
}

Write-Host "`nAll services stopped!"
Write-Host "To start the environment again, run:"
Write-Host "- Development: scripts\start_dev.ps1"
Write-Host "- Production: scripts\start_prod.ps1"
Write-Host "- Tests: scripts\run_tests.ps1" 