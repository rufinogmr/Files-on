# 📁 Files-On - Organizador Inteligente de Comprovantes

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Files-On** é um aplicativo inteligente para organização automática de comprovantes e documentos. Ele processa PDFs, imagens e documentos de texto, extrai informações importantes (data, nome, valor), detecta duplicatas e sugere uma organização inteligente de pastas.

## ✨ Funcionalidades

- 📄 **Processamento Multi-formato**: Suporta PDFs, imagens (PNG, JPG, JPEG, TIFF, BMP, GIF) e arquivos de texto
- 🔍 **OCR Inteligente**: Extrai texto de documentos escaneados e imagens usando Tesseract OCR
- 🎯 **Extração de Dados**: Identifica automaticamente:
  - 📅 **Datas** (múltiplos formatos brasileiros)
  - 👤 **Nomes** (beneficiários, clientes, favorecidos)
  - 💰 **Valores** (formato brasileiro R$)
- 🔄 **Detecção de Duplicatas**: Identifica arquivos duplicados e similares
- 📝 **Sugestão de Nomes**: Propõe nomes descritivos baseados nos dados extraídos
- 📂 **Organização Automática**: Sugere estrutura de pastas por ano/mês
- 🖥️ **Interface Gráfica Intuitiva**:
  - Barra de progresso em tempo real
  - Status detalhado do processamento
  - Contador de tempo
  - Log de operações
  - Design moderno e responsivo
- ⚡ **Processamento Assíncrono**: Interface não trava durante o processamento
- 📊 **Relatórios Detalhados**: Exportação de relatórios completos

## 📋 Pré-requisitos

### Sistema Operacional
- **Linux**: Ubuntu/Debian ou distribuições similares
- **Windows**: Windows 10 ou superior
- **macOS**: macOS 10.14 ou superior

### Dependências do Sistema

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-tk \
    tesseract-ocr \
    tesseract-ocr-por \
    poppler-utils
```

#### macOS
```bash
brew install python-tk tesseract tesseract-lang poppler
```

#### Windows
1. Instale o [Python 3.8+](https://www.python.org/downloads/) (certifique-se de marcar "Add to PATH")
2. Baixe e instale o [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)
   - Durante a instalação, adicione o idioma Português
   - Anote o caminho de instalação (geralmente `C:\Program Files\Tesseract-OCR`)
3. Baixe e instale o [Poppler for Windows](http://blog.alivate.com.au/poppler-windows/)

## 🚀 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/Files-on.git
cd Files-on
```

### 2. Crie um ambiente virtual (recomendado)
```bash
python3 -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Instale as dependências Python
```bash
pip install -r requirements.txt
```

### 4. Configure o Tesseract (apenas Windows)
Se o Tesseract não estiver no PATH do sistema, edite o arquivo `src/processors/file_processor.py` e adicione:
```python
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

## 💻 Uso

### Iniciar o aplicativo
```bash
python main.py
```

### Passo a passo

1. **Selecionar Arquivos**
   - Clique em "📂 Selecionar Arquivos" para escolher arquivos individuais
   - OU clique em "📁 Selecionar Pasta" para processar todos os arquivos de uma pasta

2. **Processar**
   - Clique em "▶️ Processar Arquivos"
   - Acompanhe o progresso na barra de progresso
   - Veja os resultados no painel de resultados

3. **Organizar**
   - Após o processamento, clique em "📋 Organizar Arquivos"
   - Escolha a pasta de destino
   - Escolha se deseja copiar ou mover os arquivos

4. **Exportar Relatório** (opcional)
   - Clique em "💾 Exportar Relatório"
   - Escolha onde salvar o relatório em texto

## 📁 Estrutura do Projeto

```
Files-on/
├── main.py                          # Ponto de entrada do aplicativo
├── requirements.txt                 # Dependências Python
├── README.md                       # Este arquivo
│
├── src/                            # Código fonte
│   ├── __init__.py
│   │
│   ├── processors/                 # Módulos de processamento
│   │   ├── __init__.py
│   │   ├── file_processor.py      # Extração de texto (OCR, PDFs)
│   │   ├── duplicate_detector.py  # Detecção de duplicatas
│   │   └── data_extractor.py      # Extração de dados estruturados
│   │
│   ├── utils/                      # Utilitários
│   │   ├── __init__.py
│   │   └── suggestion_engine.py   # Sugestões de nomes e organização
│   │
│   └── gui/                        # Interface gráfica
│       ├── __init__.py
│       └── main_gui.py            # GUI principal (Tkinter)
│
├── samples/                        # Arquivos de exemplo (opcional)
├── output/                         # Arquivos organizados (gerado)
└── tests/                          # Testes (futuro)
```

## 🎨 Capturas de Tela

### Interface Principal
A interface exibe:
- Área de seleção de arquivos
- Barra de progresso com status em tempo real
- Contador de tempo de processamento
- Painel de resultados com log detalhado
- Botões de ação claramente identificados

### Exemplo de Organização
Os arquivos são organizados automaticamente em:
```
Organizados/
├── 2024/
│   ├── 01_Janeiro/
│   │   ├── 2024-01-15_João Silva_R$150,00.pdf
│   │   └── 2024-01-20_Maria Santos_R$280,50.pdf
│   └── 02_Fevereiro/
│       └── 2024-02-10_Pedro Costa_R$1.200,00.pdf
└── Sem_Data/
    └── documento_sem_data.pdf
```

## 🔧 Configuração Avançada

### Ajustar Threshold de Similaridade
Edite `src/processors/duplicate_detector.py`:
```python
detector = DuplicateDetector(similarity_threshold=0.85)  # 0.0 a 1.0
```

### Adicionar Padrões de Extração
Edite `src/processors/data_extractor.py` para adicionar novos padrões regex:
```python
CURRENCY_PATTERNS = [
    # Adicione seus padrões aqui
]
```

### Melhorar Precisão do OCR
Para melhor precisão, instale o EasyOCR (maior download):
```bash
pip install easyocr
```
E descomente a linha no `requirements.txt`.

## 🐛 Solução de Problemas

### Erro: "Tesseract não encontrado"
- **Linux**: `sudo apt-get install tesseract-ocr tesseract-ocr-por`
- **Windows**: Verifique se o Tesseract está instalado e no PATH
- **macOS**: `brew install tesseract tesseract-lang`

### Erro: "Poppler não encontrado"
- **Linux**: `sudo apt-get install poppler-utils`
- **macOS**: `brew install poppler`
- **Windows**: Baixe e extraia o Poppler, adicione ao PATH

### OCR não reconhece português
Instale o pacote de idioma português:
```bash
# Linux
sudo apt-get install tesseract-ocr-por

# macOS
brew install tesseract-lang
```

### Interface não responde
- Certifique-se de que o Python-tk está instalado
- Verifique se há erros no terminal

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Enviar pull requests
- Melhorar a documentação

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

Desenvolvido com ❤️ por Claude Code

## 🙏 Agradecimentos

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [PyPDF2](https://github.com/py-pdf/pypdf2)
- [pdfplumber](https://github.com/jsvine/pdfplumber)
- [Pillow](https://python-pillow.org/)
- [imagehash](https://github.com/JohannesBuchner/imagehash)

## 📞 Suporte

Se você encontrar problemas ou tiver dúvidas:
1. Verifique a seção [Solução de Problemas](#-solução-de-problemas)
2. Procure por issues existentes no GitHub
3. Crie uma nova issue descrevendo o problema

---

**Files-On** - Organize seus documentos de forma inteligente! 🚀
