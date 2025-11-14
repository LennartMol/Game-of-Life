# Ensure script stops on errors
$ErrorActionPreference = "Stop"

Write-Host "Checking for UV..."

# 1. Check if UV exists
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "UV not found. Installing..."

    # --- IMPORTANT ---
    # Download installer instead of piping it directly into iex
    $installer = "$env:TEMP\uv-install.ps1"
    Invoke-WebRequest https://astral.sh/uv/install.ps1 -OutFile $installer

    # Execute installer in the SAME shell (prevents closing window)
    . $installer

    Write-Host "UV installation complete."
}

# Reload PATH (in this session)
$env:Path = [System.Environment]::GetEnvironmentVariable("Path", "User") + ";" +
            [System.Environment]::GetEnvironmentVariable("Path", "Machine")

Write-Host "Syncing environment..."
uv sync

Write-Host "Starting Game of Life..."
uv run python main.py

pause
