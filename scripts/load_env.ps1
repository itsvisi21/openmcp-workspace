# Check if environment type is provided
param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('dev', 'test', 'prod')]
    [string]$EnvType
)

# Set root directory
$scriptPath = $MyInvocation.MyCommand.Path
$scriptDir = Split-Path -Parent $scriptPath
$rootDir = Split-Path -Parent $scriptDir

# Check if environment file exists
$envFile = Join-Path $rootDir "environments\$EnvType.env"
if (-not (Test-Path $envFile)) {
    Write-Error "Error: environments\$EnvType.env not found"
    exit 1
}

Write-Host "Loading environment from $envFile"

# Load environment variables from file
Get-Content $envFile | ForEach-Object {
    if ($_ -match '^([^#][^=]+)=(.*)$') {
        $key = $matches[1].Trim()
        $value = $matches[2].Trim()
        if ($key -and $value) {
            Set-Item -Path "Env:$key" -Value $value
            Write-Host "Set: $key=$value"
        }
    }
}

# Debug: Print all environment variables
Write-Host "`nCurrent environment variables:"
Get-ChildItem Env: | ForEach-Object {
    Write-Host "$($_.Name)=$($_.Value)"
}

# Create project-specific .env files
Write-Host "`nCreating project-specific .env files..."

# Backend .env
Write-Host "Creating backend .env..."
$backendEnvFile = Join-Path $rootDir "apps\backend\.env"
$backendEnvContent = @"
# Backend Environment Configuration

# Project Settings
PROJECT_NAME=$env:BACKEND_PROJECT_NAME
VERSION=$env:BACKEND_VERSION
API_V1_STR=$env:BACKEND_API_V1_STR

# Security
JWT_SECRET_KEY=$env:JWT_SECRET_KEY
JWT_ALGORITHM=$env:JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES=$env:ACCESS_TOKEN_EXPIRE_MINUTES

# Database
DATABASE_URL=sqlite:///./test.db

# AWS Settings
AWS_ACCESS_KEY_ID=$env:AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=$env:AWS_SECRET_ACCESS_KEY
AWS_REGION=$env:AWS_REGION
AWS_BUCKET_NAME=$env:AWS_BUCKET_NAME

# CORS Settings
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]

# LLM Settings
LLM_PROVIDER=$env:DEFAULT_LLM_PROVIDER
LLM_MODEL=gpt-4
LLM_MAX_TOKENS=2000
LLM_TEMPERATURE=0.7

# Monitoring Settings
ENABLE_MONITORING=true
MONITORING_INTERVAL=60
PROMETHEUS_MULTIPROC_DIR=./prometheus_data
SENTRY_DSN=$env:SENTRY_DSN
"@

$backendEnvContent | Out-File -FilePath $backendEnvFile -Encoding UTF8
Write-Host "Backend .env file created at $backendEnvFile"
Write-Host "`nContents of backend .env file:"
Get-Content $backendEnvFile

# MCP Server .env
Write-Host "`nCreating MCP server .env..."
$mcpEnvFile = Join-Path $rootDir "apps\mcp-server\.env"
$mcpEnvContent = @"
PROJECT_NAME=$env:MCP_PROJECT_NAME
VERSION=$env:MCP_VERSION
API_V1_STR=$env:MCP_API_V1_STR
DATABASE_URL=$env:MCP_DATABASE_URL
OPENAI_API_KEY=$env:MCP_OPENAI_API_KEY
ANTHROPIC_API_KEY=$env:MCP_ANTHROPIC_API_KEY
DEFAULT_LLM_PROVIDER=$env:MCP_DEFAULT_LLM_PROVIDER
MAX_TOKENS=$env:MCP_MAX_TOKENS
ENABLE_MONITORING=$env:MCP_ENABLE_MONITORING
MONITORING_INTERVAL=$env:MCP_MONITORING_INTERVAL
BACKEND_CORS_ORIGINS=$env:MCP_BACKEND_CORS_ORIGINS
"@

$mcpEnvContent | Out-File -FilePath $mcpEnvFile -Encoding UTF8

# Dashboard .env
Write-Host "Creating dashboard .env..."
$dashboardEnvFile = Join-Path $rootDir "apps\dashboard\.env"
$dashboardEnvContent = @"
PROJECT_NAME=$env:DASHBOARD_PROJECT_NAME
VERSION=$env:DASHBOARD_VERSION
API_URL=$env:DASHBOARD_API_URL
BACKEND_URL=$env:DASHBOARD_BACKEND_URL
"@

$dashboardEnvContent | Out-File -FilePath $dashboardEnvFile -Encoding UTF8

Write-Host "`nEnvironment variables loaded successfully!" 