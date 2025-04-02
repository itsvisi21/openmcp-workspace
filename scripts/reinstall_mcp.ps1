Write-Host "Reinstalling MCP Server dependencies..."

# Set root directory
$scriptPath = $MyInvocation.MyCommand.Path
$scriptDir = Split-Path -Parent $scriptPath
$rootDir = Split-Path -Parent $scriptDir

# Change to MCP server directory
$mcpPath = Join-Path $rootDir "apps\mcp-server"
Push-Location $mcpPath

# Remove existing virtual environment if it exists
if (Test-Path ".venv") {
    Write-Host "Removing existing virtual environment..."
    Remove-Item -Recurse -Force ".venv"
}

# Create new virtual environment
Write-Host "Creating new virtual environment..."
python -m venv .venv

# Activate virtual environment
Write-Host "Activating virtual environment..."
& .\.venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "Upgrading pip..."
python -m pip install --upgrade pip

# Install dependencies
Write-Host "Installing dependencies..."
pip install -e ".[test]"

Write-Host "MCP Server dependencies reinstalled successfully!"

# Return to original directory
Pop-Location 