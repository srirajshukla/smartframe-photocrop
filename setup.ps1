# SmartFrame Setup Script

Write-Host "--- SmartFrame Setup ---" -ForegroundColor Cyan

# 1. Check for uv
if (!(Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "'uv' is not installed." -ForegroundColor Yellow
    $choice = Read-Host "Would you like to install 'uv' automatically now? (y/n)"
    
    if ($choice -eq 'y') {
        Write-Host "Installing 'uv'..." -ForegroundColor Cyan
        powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
        
        # Add to current session path so we can use it immediately
        $env:Path += ";$HOME\.local\bin"
        
        if (!(Get-Command uv -ErrorAction SilentlyContinue)) {
            Write-Host "Installation failed or 'uv' is not in the PATH. Please restart your terminal and try again." -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "Please install 'uv' manually from https://docs.astral.sh/uv/ to proceed." -ForegroundColor Red
        exit 1
    }
}

Write-Host "Checking/Installing dependencies..." -ForegroundColor Yellow
uv sync

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Dependency sync failed." -ForegroundColor Red
    exit 1
}

Write-Host "`n--- Setup Complete! ---" -ForegroundColor Green
Write-Host "You can now run the application using: .\run.ps1"
