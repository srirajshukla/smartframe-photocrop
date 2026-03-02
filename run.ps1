# SmartFrame Run Script

# 1. Check for uv
if (!(Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "Error: 'uv' is not installed. Please install it from https://docs.astral.sh/uv/" -ForegroundColor Red
    exit 1
}

# Run the app
uv run main.py
