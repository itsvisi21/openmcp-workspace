# Install dependencies for all projects
Write-Host "Installing dependencies for all projects..."

# Set root directory
$scriptPath = $MyInvocation.MyCommand.Path
$scriptDir = Split-Path -Parent $scriptPath
$rootDir = Split-Path -Parent $scriptDir

Write-Host "Debug: Script directory = $scriptDir"
Write-Host "Debug: Root directory = $rootDir"

function Install-NodeDependencies {
    param (
        [string]$projectName,
        [string]$projectPath
    )
    
    Write-Host "`nInstalling $projectName Node.js dependencies..."
    Write-Host "Debug: Attempting to change to directory: $projectPath"
    
    # Change to project directory
    try {
        Push-Location $projectPath
        Write-Host "Debug: Current directory = $(Get-Location)"
    }
    catch {
        Write-Error "Failed to change to $projectName directory"
        Write-Host "Debug: Directory contents of $(Split-Path -Parent $projectPath):"
        Get-ChildItem $(Split-Path -Parent $projectPath)
        return $false
    }
    
    # Check if Node.js is installed
    try {
        $nodeVersion = node --version
        Write-Host "Debug: Node.js version: $nodeVersion"
    }
    catch {
        Write-Error "Node.js is not installed. Please install Node.js first."
        Pop-Location
        return $false
    }
    
    # Install dependencies
    Write-Host "Debug: Installing $projectName Node.js dependencies..."
    try {
        npm install
        Write-Host "Debug: Node.js dependencies installed successfully"
    }
    catch {
        Write-Error "Failed to install Node.js dependencies for $projectName"
        Write-Error $_.Exception.Message
        Pop-Location
        return $false
    }
    
    Pop-Location
    return $true
}

function Install-ProjectDependencies {
    param (
        [string]$projectName,
        [string]$projectPath,
        [string]$projectType = "python"
    )
    
    if ($projectType -eq "node") {
        return Install-NodeDependencies -projectName $projectName -projectPath $projectPath
    }
    
    Write-Host "`nInstalling $projectName dependencies..."
    Write-Host "Debug: Attempting to change to directory: $projectPath"
    
    # Change to project directory
    try {
        Push-Location $projectPath
        Write-Host "Debug: Current directory = $(Get-Location)"
    }
    catch {
        Write-Error "Failed to change to $projectName directory"
        Write-Host "Debug: Directory contents of $(Split-Path -Parent $projectPath):"
        Get-ChildItem $(Split-Path -Parent $projectPath)
        return $false
    }
    
    # Create virtual environment if it doesn't exist
    if (-not (Test-Path ".venv")) {
        Write-Host "Creating virtual environment for $projectName..."
        try {
            python -m venv .venv
            Write-Host "Debug: Virtual environment created successfully"
        }
        catch {
            Write-Error "Failed to create virtual environment for $projectName"
            Write-Host "Debug: Python version:"
            python --version
            Pop-Location
            return $false
        }
    }
    
    # Activate virtual environment
    Write-Host "Debug: Activating virtual environment..."
    try {
        & .\.venv\Scripts\Activate.ps1
    }
    catch {
        Write-Error "Failed to activate virtual environment for $projectName"
        Write-Host "Debug: Checking .venv\Scripts directory:"
        Get-ChildItem .venv\Scripts
        Pop-Location
        return $false
    }
    
    # Install dependencies
    Write-Host "Debug: Upgrading pip..."
    python -m pip install --upgrade pip
    
    if (Test-Path "requirements.txt") {
        Write-Host "Debug: Installing $projectName requirements..."
        try {
            # For MCP Server, we need to ensure we install the latest versions
            if ($projectName -eq "MCP Server") {
                Write-Host "Debug: Installing MCP Server dependencies with --upgrade flag..."
                pip install --upgrade -r requirements.txt
                
                # Install specific versions that are required
                Write-Host "Debug: Installing specific required versions..."
                pip install --upgrade "fastapi>=0.109.0" "pydantic>=2.6.0" "pydantic-settings>=2.1.0" "uvicorn>=0.27.0"
                
                # Reinstall the project in editable mode if setup.py exists
                if (Test-Path "setup.py") {
                    Write-Host "Debug: Installing project in editable mode..."
                    pip install -e .
                }
            }
            else {
                pip install -r requirements.txt
            }
        }
        catch {
            Write-Error "Failed to install dependencies for $projectName"
            Write-Error $_.Exception.Message
            deactivate
            Pop-Location
            return $false
        }
    }
    else {
        Write-Error "requirements.txt not found in $projectName directory"
        deactivate
        Pop-Location
        return $false
    }
    
    deactivate
    Pop-Location
    return $true
}

# Install dependencies for each project
$projects = @(
    @{ Name = "Backend"; Path = "$rootDir\apps\backend"; Type = "python" },
    @{ Name = "MCP Server"; Path = "$rootDir\apps\mcp-server"; Type = "python" },
    @{ Name = "Library"; Path = "$rootDir\apps\libraries"; Type = "python" },
    @{ Name = "Dashboard"; Path = "$rootDir\apps\dashboard"; Type = "node" }
)

$success = $true
foreach ($project in $projects) {
    if (-not (Install-ProjectDependencies -projectName $project.Name -projectPath $project.Path -projectType $project.Type)) {
        $success = $false
        break
    }
}

if ($success) {
    Write-Host "`nAll dependencies installed successfully!"
}
else {
    Write-Error "`nFailed to install dependencies. Please check the errors above."
    exit 1
} 