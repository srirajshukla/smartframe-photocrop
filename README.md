# SmartFrame

SmartFrame is a Python application for AI-powered portrait editing, background removal, and professional photo formatting.

## Features

- AI Face Detection and Auto-Cropping.
- High-quality Background Removal (u2net, isnet, birefnet).
- Real-time portrait enhancements (Brightness, Contrast, Skin Smoothing).
- Export to single photo or 4x6 print sheets.

## Installation and Setup (Windows)

The application uses 'uv' for fast dependency management. A setup script is provided to automate the process.

1. Clone or download the repository.
2. Open PowerShell in the project directory.
3. Run the setup script:
   ```powershell
   .\setup.ps1
   ```
   Note: If 'uv' is not installed, the script will prompt to install it for you.

## Running the Application

After setup is complete, launch the application using:
```powershell
.\run.ps1
```

## Manual Usage (CLI)

If you prefer using the command line directly:
- Sync dependencies: `uv sync`
- Run app: `uv run main.py`
