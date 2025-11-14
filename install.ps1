# Install UV if not installed
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "UV not found. Installing..."
    irm https://astral.sh/uv/install.ps1 | iex
}

# Sync project (installs Python + deps)
uv sync

# Run the simulation
uv run python main.py