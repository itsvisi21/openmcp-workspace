Write-Host "Creating OpenMCP Project Structure..."

# Set root directory
$scriptPath = $MyInvocation.MyCommand.Path
$scriptDir = Split-Path -Parent $scriptPath
$rootDir = Split-Path -Parent $scriptDir

# Create main directories
Write-Host "Creating main directories..."
New-Item -ItemType Directory -Force -Path @(
    Join-Path $rootDir "apps",
    Join-Path $rootDir "environments",
    Join-Path $rootDir "scripts"
) | Out-Null

# Create app directories
Write-Host "Creating app directories..."
$appsDir = Join-Path $rootDir "apps"

# Backend structure
Write-Host "Creating Backend structure..."
$backendDirs = @(
    "backend",
    "backend\src",
    "backend\tests",
    "backend\src\app",
    "backend\src\app\api",
    "backend\src\app\core",
    "backend\src\app\db",
    "backend\src\app\models",
    "backend\src\app\schemas",
    "backend\src\app\services"
)

# MCP Server structure
Write-Host "Creating MCP Server structure..."
$mcpDirs = @(
    "mcp-server",
    "mcp-server\src",
    "mcp-server\tests",
    "mcp-server\src\app",
    "mcp-server\src\app\api",
    "mcp-server\src\app\core",
    "mcp-server\src\app\services"
)

# Libraries structure
Write-Host "Creating Libraries structure..."
$libraryDirs = @(
    "libraries",
    "libraries\src",
    "libraries\tests"
)

# Dashboard structure
Write-Host "Creating Dashboard structure..."
$dashboardDirs = @(
    "dashboard",
    "dashboard\src",
    "dashboard\src\components",
    "dashboard\src\pages",
    "dashboard\src\__tests__"
)

# Create all directories
$allDirs = $backendDirs + $mcpDirs + $libraryDirs + $dashboardDirs
foreach ($dir in $allDirs) {
    New-Item -ItemType Directory -Force -Path (Join-Path $appsDir $dir) | Out-Null
}

# Create initial files
Write-Host "Creating initial files..."

# Backend files
Write-Host "Creating Backend files..."
$backendFiles = @(
    "backend\requirements.txt",
    "backend\pyproject.toml",
    "backend\src\app\__init__.py",
    "backend\src\app\main.py",
    "backend\src\app\core\config.py",
    "backend\src\app\core\monitoring.py",
    "backend\src\app\db\base.py",
    "backend\src\app\db\session.py",
    "backend\src\app\models\__init__.py",
    "backend\src\app\schemas\__init__.py",
    "backend\src\app\services\__init__.py"
)

# MCP Server files
Write-Host "Creating MCP Server files..."
$mcpFiles = @(
    "mcp-server\requirements.txt",
    "mcp-server\pyproject.toml",
    "mcp-server\src\app\__init__.py",
    "mcp-server\src\app\main.py",
    "mcp-server\src\app\api\__init__.py",
    "mcp-server\src\app\core\__init__.py",
    "mcp-server\src\app\services\__init__.py"
)

# Libraries files
Write-Host "Creating Libraries files..."
$libraryFiles = @(
    "libraries\pyproject.toml",
    "libraries\src\__init__.py",
    "libraries\src\library.py",
    "libraries\tests\__init__.py",
    "libraries\tests\test_library.py"
)

# Dashboard files
Write-Host "Creating Dashboard files..."
$dashboardFiles = @(
    "dashboard\package.json",
    "dashboard\tsconfig.json",
    "dashboard\src\App.tsx",
    "dashboard\src\index.tsx",
    "dashboard\src\__tests__\App.test.tsx"
)

# Create all files
$allFiles = $backendFiles + $mcpFiles + $libraryFiles + $dashboardFiles
foreach ($file in $allFiles) {
    New-Item -ItemType File -Force -Path (Join-Path $appsDir $file) | Out-Null
}

# Environment files
Write-Host "Creating environment files..."
$envFiles = @(
    "environments\dev.env",
    "environments\test.env",
    "environments\prod.env"
)

foreach ($file in $envFiles) {
    New-Item -ItemType File -Force -Path (Join-Path $rootDir $file) | Out-Null
}

Write-Host "`nProject structure created successfully!"
Write-Host "`nNext steps:"
Write-Host "1. Run scripts\setup_dev.ps1 to set up the development environment"
Write-Host "2. Update the environment files with your configuration"
Write-Host "3. Run scripts\start_dev.ps1 to start the development servers" 