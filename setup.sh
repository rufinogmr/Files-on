#!/bin/bash
# Setup script for Files-On on Linux/macOS

echo "================================================"
echo "Files-On - Instalação Automática"
echo "================================================"
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3.8 ou superior."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Python encontrado: $(python3 --version)"

# Check for system dependencies
echo ""
echo "Verificando dependências do sistema..."

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Sistema: Linux"
    echo ""
    echo "Instalando dependências do sistema (requer sudo)..."
    sudo apt-get update
    sudo apt-get install -y python3-pip python3-tk tesseract-ocr tesseract-ocr-por poppler-utils
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Sistema: macOS"
    echo ""
    if ! command -v brew &> /dev/null; then
        echo "❌ Homebrew não encontrado. Instale em: https://brew.sh"
        exit 1
    fi
    echo "Instalando dependências via Homebrew..."
    brew install python-tk tesseract tesseract-lang poppler
else
    echo "⚠️  Sistema operacional não suportado pelo script automático"
    echo "Por favor, siga as instruções manuais no README.md"
    exit 1
fi

# Create virtual environment
echo ""
echo "Criando ambiente virtual..."
python3 -m venv venv

# Activate virtual environment
echo "Ativando ambiente virtual..."
source venv/bin/activate

# Install Python dependencies
echo ""
echo "Instalando dependências Python..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "================================================"
echo "✅ Instalação concluída com sucesso!"
echo "================================================"
echo ""
echo "Para iniciar o aplicativo:"
echo "  1. Ative o ambiente virtual: source venv/bin/activate"
echo "  2. Execute: python main.py"
echo ""
echo "Ou use o script run.sh"
echo "================================================"
