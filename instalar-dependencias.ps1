# Files-On - Instalador Automático de Dependências
# Execute como Administrador

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Files-On - Instalador de Dependências" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se está rodando como Administrador
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ERRO: Este script precisa ser executado como Administrador!" -ForegroundColor Red
    Write-Host "Clique direito no arquivo e selecione 'Executar como Administrador'" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Pressione qualquer tecla para sair..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host "[1/2] Verificando Tesseract OCR..." -ForegroundColor Yellow

$tesseractPath = "C:\Program Files\Tesseract-OCR\tesseract.exe"
if (Test-Path $tesseractPath) {
    Write-Host "  OK: Tesseract ja instalado!" -ForegroundColor Green
} else {
    Write-Host "  Tesseract nao encontrado!" -ForegroundColor Red
    Write-Host "  Abrindo pagina de download..." -ForegroundColor Yellow
    Start-Process "https://github.com/UB-Mannheim/tesseract/wiki"
    Write-Host ""
    Write-Host "  Por favor:" -ForegroundColor Yellow
    Write-Host "    1. Baixe e instale o Tesseract" -ForegroundColor Yellow
    Write-Host "    2. Durante instalacao, marque 'Portuguese' como idioma adicional" -ForegroundColor Yellow
    Write-Host "    3. Execute este script novamente apos a instalacao" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Pressione qualquer tecla para sair..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host ""
Write-Host "[2/2] Verificando Poppler..." -ForegroundColor Yellow

$popplerPath = "C:\Program Files\poppler\Library\bin\pdftoppm.exe"
if (Test-Path $popplerPath) {
    Write-Host "  OK: Poppler ja instalado!" -ForegroundColor Green

    # Verificar se está no PATH
    $envPath = [Environment]::GetEnvironmentVariable("Path", "Machine")
    if ($envPath -notlike "*poppler*") {
        Write-Host "  Adicionando Poppler ao PATH..." -ForegroundColor Yellow
        $newPath = $envPath + ";C:\Program Files\poppler\Library\bin"
        [Environment]::SetEnvironmentVariable("Path", $newPath, "Machine")
        Write-Host "  OK: Poppler adicionado ao PATH!" -ForegroundColor Green
    }
} else {
    Write-Host "  Poppler nao encontrado!" -ForegroundColor Red
    Write-Host "  Abrindo pagina de download..." -ForegroundColor Yellow
    Start-Process "https://github.com/oschwartz10612/poppler-windows/releases/"
    Write-Host ""
    Write-Host "  Por favor:" -ForegroundColor Yellow
    Write-Host "    1. Baixe o arquivo Release-XX.XX.X-0.zip (mais recente)" -ForegroundColor Yellow
    Write-Host "    2. Extraia para C:\Program Files\poppler" -ForegroundColor Yellow
    Write-Host "    3. Execute este script novamente" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Pressione qualquer tecla para sair..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "TUDO PRONTO!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Voce pode agora executar Files-On.exe!" -ForegroundColor Green
Write-Host ""
Write-Host "IMPORTANTE: Reinicie o computador para aplicar as mudancas no PATH." -ForegroundColor Yellow
Write-Host ""
Write-Host "Pressione qualquer tecla para sair..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
