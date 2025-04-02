Write-Host "Setting up OpenMCP Development Environment..."
Write-Host "Current directory: $(Get-Location)"

# Set root directory
$scriptPath = $MyInvocation.MyCommand.Path
$scriptDir = Split-Path -Parent $scriptPath
$rootDir = Split-Path -Parent $scriptDir

# Check Python installation
Write-Host "Checking Python installation..."
try {
    $pythonVersion = python --version
    Write-Host "Python version: $pythonVersion"
} catch {
    Write-Error "Error: Python is not installed or not in PATH"
    exit 1
}

# Check Node.js installation
Write-Host "Checking Node.js installation..."
try {
    $nodeVersion = node --version
    Write-Host "Node.js version: $nodeVersion"
} catch {
    Write-Error "Error: Node.js is not installed or not in PATH"
    exit 1
}

# Check npm installation
Write-Host "Checking npm installation..."
try {
    $npmVersion = npm --version
    Write-Host "npm version: $npmVersion"
} catch {
    Write-Error "Error: npm is not installed or not in PATH"
    exit 1
}

# Create environments directory if it doesn't exist
$envDir = Join-Path $rootDir "environments"
if (-not (Test-Path $envDir)) {
    Write-Host "Creating environments directory..."
    New-Item -ItemType Directory -Force -Path $envDir | Out-Null
}

# Create environment files if they don't exist
Write-Host "Setting up environment files..."
$envFiles = @(
    "dev.env",
    "test.env",
    "prod.env"
)

foreach ($file in $envFiles) {
    $envFile = Join-Path $envDir $file
    if (-not (Test-Path $envFile)) {
        Write-Host "Creating $file..."
        New-Item -ItemType File -Force -Path $envFile | Out-Null
        Write-Host "Created $file. Please update with your configuration."
    }
}

# Function to setup Python project
function Setup-PythonProject {
    param (
        [string]$ProjectName,
        [string]$ProjectPath,
        [string]$InstallCommand
    )
    
    Write-Host "Setting up $ProjectName..."
    Push-Location $ProjectPath
    
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
    Invoke-Expression $InstallCommand
    
    Pop-Location
}

# Setup Backend
Setup-PythonProject -ProjectName "Backend" -ProjectPath (Join-Path $rootDir "apps\backend") -InstallCommand "pip install -r requirements.txt"

# Setup MCP Server
Setup-PythonProject -ProjectName "MCP Server" -ProjectPath (Join-Path $rootDir "apps\mcp-server") -InstallCommand "pip install -r requirements.txt"

# Setup Libraries
Setup-PythonProject -ProjectName "Libraries" -ProjectPath (Join-Path $rootDir "apps\libraries") -InstallCommand "pip install -e '.[test]'"

# Setup Dashboard
Write-Host "Setting up Dashboard..."
$dashboardPath = Join-Path $rootDir "apps\dashboard"
Push-Location $dashboardPath

# Remove existing node_modules and package-lock.json if they exist
if (Test-Path "node_modules") {
    Write-Host "Removing existing node_modules..."
    Remove-Item -Recurse -Force "node_modules"
}

if (Test-Path "package-lock.json") {
    Write-Host "Removing existing package-lock.json..."
    Remove-Item -Force "package-lock.json"
}

# Install dependencies
Write-Host "Installing npm dependencies..."
npm install --verbose

Pop-Location

# Load development environment
Write-Host "Loading development environment..."
& (Join-Path $scriptDir "load_env.ps1") -EnvType "dev"

Write-Host "`nDevelopment environment setup complete!"
Write-Host "`nNext steps:"
Write-Host "1. Update the environment files in the environments directory with your configuration"
Write-Host "2. Run scripts\start_dev.ps1 to start the development servers"
Write-Host "`nNote: Make sure to set your API keys and other sensitive information in the environment files." 