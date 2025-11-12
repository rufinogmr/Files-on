@echo off
echo ================================================
echo Files-On - Construtor de Executavel
echo ================================================
echo.

echo [1/4] Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo [2/4] Instalando PyInstaller...
pip install pyinstaller

echo [3/4] Construindo executavel...
echo Isso pode levar alguns minutos...
pyinstaller --name="Files-On" ^
    --onefile ^
    --windowed ^
    --icon=NONE ^
    --add-data "src;src" ^
    --hidden-import=tkinter ^
    --hidden-import=PIL._tkinter_finder ^
    main.py

echo.
echo [4/4] Limpando arquivos temporarios...
rmdir /s /q build
del /q Files-On.spec

echo.
echo ================================================
echo PRONTO! Executavel criado em: dist\Files-On.exe
echo ================================================
echo.
echo IMPORTANTE: O computador de destino precisa ter:
echo  1. Tesseract OCR instalado
echo  2. Poppler instalado
echo.
echo Pressione qualquer tecla para sair...
pause > nul
