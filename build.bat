@echo off
echo === Markscan BW Image Processor Build Script ===
echo.
echo 1. Activating virtual environment...
call .\venv\Scripts\activate.bat

echo.
echo 2. Updating requirements.txt...
pip freeze > requirements.txt

echo.
echo 3. Generating license information...
pip-licenses --format=markdown --with-license-file --no-license-path --output-file=LICENSES.md

echo.
echo 4. Building executable with PyInstaller...
pyinstaller --name markscan_bw --onefile --windowed --clean markscan_bw.py

echo.
echo === Build completed! ===
echo Executable available in the "dist" folder
echo.
