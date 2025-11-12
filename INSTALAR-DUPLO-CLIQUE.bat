@echo off
:: Files-On - Instalador Super Simples
:: Apenas clique duas vezes neste arquivo!

title Files-On - Instalador
color 0A

echo.
echo ================================================
echo    FILES-ON - INSTALADOR AUTOMATICO
echo ================================================
echo.
echo Preparando instalacao...
echo.
timeout /t 2 /nobreak >nul

:: Verificar se esta rodando como Admin
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo [ATENCAO] Este instalador precisa de permissao de Administrador
    echo.
    echo Clique com botao DIREITO neste arquivo
    echo e escolha "Executar como administrador"
    echo.
    pause
    exit
)

echo [OK] Executando como Administrador
echo.

:: Criar pasta de instalacao
set "INSTALL_DIR=%ProgramFiles%\Files-On"
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

echo [1/5] Verificando Tesseract OCR...
if exist "C:\Program Files\Tesseract-OCR\tesseract.exe" (
    echo       [OK] Tesseract ja instalado!
) else (
    echo       [AVISO] Tesseract nao encontrado
    echo.
    echo Abrindo pagina de download do Tesseract...
    start https://github.com/UB-Mannheim/tesseract/wiki
    echo.
    echo ================================================
    echo IMPORTANTE: Siga estes passos:
    echo ================================================
    echo 1. Baixe o instalador do Tesseract
    echo 2. Execute o instalador
    echo 3. Durante instalacao, marque "Portuguese"
    echo 4. Aguarde instalacao terminar
    echo 5. Execute este instalador novamente
    echo ================================================
    echo.
    pause
    exit
)

echo.
echo [2/5] Verificando Poppler...
if exist "C:\Program Files\poppler\Library\bin\pdftoppm.exe" (
    echo       [OK] Poppler ja instalado!
) else (
    echo       [AVISO] Poppler nao encontrado
    echo.
    echo Abrindo pagina de download do Poppler...
    start https://github.com/oschwartz10612/poppler-windows/releases/
    echo.
    echo ================================================
    echo IMPORTANTE: Siga estes passos:
    echo ================================================
    echo 1. Baixe o arquivo Release-XX.XX.X-0.zip
    echo 2. Extraia o conteudo
    echo 3. Copie a pasta extraida para:
    echo    C:\Program Files\poppler
    echo 4. Execute este instalador novamente
    echo ================================================
    echo.
    pause
    exit
)

echo.
echo [3/5] Adicionando Poppler ao PATH do sistema...
setx /M PATH "%PATH%;C:\Program Files\poppler\Library\bin" >nul 2>&1
if %errorLevel% equ 0 (
    echo       [OK] Poppler adicionado ao PATH
) else (
    echo       [AVISO] Nao foi possivel adicionar ao PATH automaticamente
)

echo.
echo [4/5] Copiando arquivos do Files-On...
if exist "dist\Files-On.exe" (
    copy /Y "dist\Files-On.exe" "%INSTALL_DIR%\" >nul
    copy /Y "LEIA-ME.txt" "%INSTALL_DIR%\" >nul
    echo       [OK] Arquivos copiados para %INSTALL_DIR%
) else (
    echo       [ERRO] Arquivo Files-On.exe nao encontrado!
    echo       Execute primeiro o build.bat para criar o executavel
    pause
    exit
)

echo.
echo [5/5] Criando atalhos...

:: Atalho no Desktop
set "SHORTCUT_DESKTOP=%USERPROFILE%\Desktop\Files-On.lnk"
powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%SHORTCUT_DESKTOP%'); $s.TargetPath = '%INSTALL_DIR%\Files-On.exe'; $s.Save()"
echo       [OK] Atalho criado na Area de Trabalho

:: Atalho no Menu Iniciar
set "SHORTCUT_START=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Files-On.lnk"
powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%SHORTCUT_START%'); $s.TargetPath = '%INSTALL_DIR%\Files-On.exe'; $s.Save()"
echo       [OK] Atalho criado no Menu Iniciar

echo.
echo ================================================
echo          INSTALACAO CONCLUIDA!
echo ================================================
echo.
echo Files-On foi instalado em:
echo %INSTALL_DIR%
echo.
echo Um atalho foi criado na sua Area de Trabalho
echo.
echo IMPORTANTE: Reinicie o computador antes de usar!
echo.
echo ================================================
echo.
choice /C SN /M "Deseja executar o Files-On agora"
if errorlevel 2 goto end
if errorlevel 1 goto run

:run
start "" "%INSTALL_DIR%\Files-On.exe"

:end
echo.
echo Obrigado por usar Files-On!
timeout /t 3 >nul
exit
