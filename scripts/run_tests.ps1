# Run tests for all projects
Write-Host "Running tests for all projects..."

# Set root directory
$scriptPath = $MyInvocation.MyCommand.Path
$scriptDir = Split-Path -Parent $scriptPath
$rootDir = Split-Path -Parent $scriptDir

Write-Host "Debug: Script directory = $scriptDir"
Write-Host "Debug: Root directory = $rootDir"

function Run-NodeTests {
    param (
        [string]$projectName,
        [string]$projectPath
    )
    
    Write-Host "`nRunning $projectName tests..."
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
    
    # Run tests with coverage
    Write-Host "Debug: Running tests with coverage..."
    try {
        npm run coverage
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Tests failed for $projectName"
            Pop-Location
            return $false
        }
    }
    catch {
        Write-Error "Failed to run tests for $projectName"
        Write-Error $_.Exception.Message
        Pop-Location
        return $false
    }
    
    Write-Host "$projectName tests completed successfully!"
    Pop-Location
    return $true
}

function Run-ProjectTests {
    param (
        [string]$projectName,
        [string]$projectPath,
        [string]$projectType = "python"
    )
    
    if ($projectType -eq "node") {
        return Run-NodeTests -projectName $projectName -projectPath $projectPath
    }
    
    Write-Host "`nRunning $projectName tests..."
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
    
    # Check for virtual environment
    if (-not (Test-Path ".venv")) {
        Write-Error "Error: Virtual environment not found for $projectName"
        Pop-Location
        return $false
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
    
    # Run tests with coverage
    Write-Host "Debug: Running tests with coverage..."
    try {
        pytest --cov=src --cov-report=html
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Tests failed for $projectName"
            deactivate
            Pop-Location
            return $false
        }
    }
    catch {
        Write-Error "Failed to run tests for $projectName"
        Write-Error $_.Exception.Message
        deactivate
        Pop-Location
        return $false
    }
    
    deactivate
    Write-Host "$projectName tests completed successfully!"
    Pop-Location
    return $true
}

# Run tests for each project
$projects = @(
    @{ Name = "Backend"; Path = "$rootDir\apps\backend"; Type = "python" },
    @{ Name = "MCP Server"; Path = "$rootDir\apps\mcp-server"; Type = "python" },
    @{ Name = "Library"; Path = "$rootDir\apps\libraries"; Type = "python" },
    @{ Name = "Dashboard"; Path = "$rootDir\apps\dashboard"; Type = "node" }
)

$success = $true
foreach ($project in $projects) {
    if (-not (Run-ProjectTests -projectName $project.Name -projectPath $project.Path -projectType $project.Type)) {
        $success = $false
        break
    }
}

if ($success) {
    Write-Host "`nAll tests completed successfully!"
}
else {
    Write-Error "`nFailed to run tests. Please check the errors above."
    exit 1
} 