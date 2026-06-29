<div align="center">
  <h1>📁 Files-On</h1>
  <p><strong>Automação Inteligente para Organização de Comprovantes e Documentos</strong></p>

  [![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)](https://www.python.org/)
  [![Tesseract OCR](https://img.shields.io/badge/OCR-Tesseract-orange)](#)
  [![Tkinter](https://img.shields.io/badge/GUI-Tkinter-lightgrey)](#)
  [![Status](https://img.shields.io/badge/Status-Stable-success)](#)
  [![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
</div>

<br>

O **Files-On** é uma ferramenta de automação desktop desenvolvida em Python para resolver um problema comum em setores financeiros e administrativos: o caos de comprovantes e recibos desorganizados. 

Utilizando **Visão Computacional (OCR)** e algoritmos de similaridade, o aplicativo "lê" seus documentos, extrai as informações cruciais e organiza tudo automaticamente em pastas padronizadas, detectando até mesmo arquivos duplicados.

---

## ✨ Features Principais de Automação

- 🔍 **Extração de Dados via OCR:** Lê PDFs e imagens (usando Tesseract OCR) e identifica automaticamente **Datas**, **Nomes** (favorecidos/clientes) e **Valores (R$)**.
- 🔄 **Detecção Avançada de Duplicatas:** Não confia apenas no nome do arquivo. O sistema usa *Image Hashing* e análise de conteúdo para encontrar comprovantes duplicados, mesmo que tenham sido salvos com nomes diferentes.
- 📂 **Organização Estruturada:** Sugere e cria automaticamente uma árvore de diretórios baseada em `Ano/Mês` (ex: `2024/01_Janeiro/`).
- 🏷️ **Renomeação Padronizada:** Sugere novos nomes para os arquivos no padrão: `[Data]_[Nome]_[Valor].pdf`.
- ⚡ **Processamento Assíncrono:** Utiliza *threading* para processar dezenas de arquivos em lote sem travar a interface gráfica.
- 📦 **Pronto para o Usuário Final:** Inclui scripts (`PyInstaller`) para gerar um executável `.exe` e um instalador simples (estilo "Next > Next > Finish") para usuários que não têm Python instalado.

---

## 🏗️ Arquitetura do Projeto

O código foi desenhado de forma modular, separando a interface gráfica dos motores de processamento:

```text
src/
├── processors/                 # Motores de automação
│   ├── file_processor.py       # Extração de texto (OCR e PDFs)
│   ├── duplicate_detector.py   # Algoritmos de hash e similaridade
│   └── data_extractor.py       # Regex para extração de dados estruturados
├── utils/                      
│   └── suggestion_engine.py    # Lógica de renomeação e roteamento de pastas
└── gui/                        
    └── main_gui.py             # Interface Desktop (Tkinter)
```

**Principais Bibliotecas:** `pytesseract` (OCR), `pdfplumber` e `PyPDF2` (Manipulação de PDF), `Pillow` (Processamento de Imagens), `imagehash` (Detecção de duplicatas).

---

## 📸 Preview da Interface

*(Adicione aqui um GIF ou Screenshot do seu aplicativo rodando, mostrando a barra de progresso e a lista de arquivos processados)*
> `![Files-On Demo](docs/demo.gif)`

---

## 🚀 Como Instalar e Rodar (Para Desenvolvedores)

### Pré-requisitos do Sistema
Para que a extração de texto funcione, você precisa ter os motores base instalados no seu SO:
- **Tesseract OCR** (com pacote de idioma Português `por`)
- **Poppler** (para conversão de PDF para imagem)

### Setup do Ambiente Python

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/rufinogmr/Files-on.git
   cd Files-on
   ```

2. **Crie o ambiente virtual e instale as dependências:**
   ```bash
   python -m venv venv
   # Windows: venv\Scripts\activate
   # Linux/Mac: source venv/bin/activate
   
   pip install -r requirements.txt
   ```

3. **Rode a aplicação:**
   ```bash
   python main.py
   ```

---

## 📦 Como Gerar o Executável (.exe)

Se você quiser distribuir o aplicativo para a equipe do financeiro/administrativo que não usa Python:

1. Rode o script de build:
   ```cmd
   build.bat
   ```
2. O arquivo `Files-On.exe` será gerado na pasta `dist/`.
3. Para instalar em outra máquina, basta enviar o executável junto com o script `INSTALAR-DUPLO-CLIQUE.bat`, que baixa automaticamente o Tesseract e o Poppler na máquina do usuário.

---

## 🤝 Como Contribuir

Contribuições são bem-vindas! Se você quer melhorar a precisão do Regex de extração ou adicionar suporte a novos formatos de comprovantes:

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaExtracao`)
3. Commit suas mudanças (`git commit -m 'feat: Adiciona suporte a comprovantes do Banco X'`)
4. Push para a branch (`git push origin feature/NovaExtracao`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---
<div align="center">
  <p>Desenvolvido com 🤖 por <a href="https://github.com/rufinogmr">Guilherme Rufino</a></p>
</div>
