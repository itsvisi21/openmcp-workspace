Write-Host "Starting OpenMCP Production Environment..."

# Set root directory
$scriptPath = $MyInvocation.MyCommand.Path
$scriptDir = Split-Path -Parent $scriptPath
$rootDir = Split-Path -Parent $scriptDir

# Load production environment
Write-Host "Loading production environment..."
& (Join-Path $scriptDir "load_env.ps1") -EnvType "prod"

# Check if virtual environments exist
$backendVenv = Join-Path $rootDir "apps\backend\.venv"
$mcpVenv = Join-Path $rootDir "apps\mcp-server\.venv"

if (-not (Test-Path $backendVenv)) {
    Write-Error "Error: Backend virtual environment not found. Please run setup_dev.ps1 first."
    exit 1
}

if (-not (Test-Path $mcpVenv)) {
    Write-Error "Error: MCP server virtual environment not found. Please run setup_dev.ps1 first."
    exit 1
}

# Start the services
Write-Host "Starting services..."

# Function to start a service in a new window
function Start-ServiceWindow {
    param (
        [string]$Title,
        [string]$Command
    )
    
    $process = Start-Process powershell -ArgumentList "-NoExit", "-Command", $Command -WindowStyle Normal
    Write-Host "Started $Title (PID: $($process.Id))"
}

# Start backend server
$backendCommand = "cd '$(Join-Path $rootDir "apps\backend")'; .\.venv\Scripts\Activate.ps1; `$env:PYTHONPATH='src'; uvicorn src.app.main:app --host 0.0.0.0 --port 8000"
Start-ServiceWindow -Title "Backend Server" -Command $backendCommand

# Start MCP server
$mcpCommand = "cd '$(Join-Path $rootDir "apps\mcp-server")'; .\.venv\Scripts\Activate.ps1; uvicorn app.main:app --host 0.0.0.0 --port 8001"
Start-ServiceWindow -Title "MCP Server" -Command $mcpCommand

# Start dashboard (production build)
$dashboardCommand = "cd '$(Join-Path $rootDir "apps\dashboard")'; npm run build; npm run preview"
Start-ServiceWindow -Title "Dashboard" -Command $dashboardCommand

Write-Host "`nProduction environment started!"
Write-Host "Services running at:"
Write-Host "- Backend: http://localhost:8000"
Write-Host "- MCP Server: http://localhost:8001"
Write-Host "- Dashboard: http://localhost:4173" 