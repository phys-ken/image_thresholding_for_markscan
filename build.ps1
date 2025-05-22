# Markscan BW Image Processor Build Script

Write-Host "=== Markscan BW Image Processor Build Script ===" -ForegroundColor Cyan
Write-Host ""

Write-Host "1. Activating virtual environment..." -ForegroundColor Green
& .\venv\Scripts\Activate.ps1

Write-Host ""
Write-Host "2. Updating requirements.txt..." -ForegroundColor Green
pip freeze > requirements.txt

Write-Host ""
Write-Host "3. Generating license information..." -ForegroundColor Green
pip-licenses --format=markdown --with-license-file --no-license-path --output-file=LICENSES.md

Write-Host ""
Write-Host "4. Building executable with PyInstaller..." -ForegroundColor Green
pyinstaller --name markscan_bw --onefile --windowed --clean markscan_bw.py

Write-Host ""
Write-Host "=== Build completed! ===" -ForegroundColor Cyan
Write-Host "Executable available in the 'dist' folder"
Write-Host ""
