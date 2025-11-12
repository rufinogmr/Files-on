# 📦 Files-On - Instalação Simples (Para Usuários Finais)

## ✅ **Instalação Rápida (3 passos)**

### **1️⃣ Instale o Tesseract OCR**

É necessário para ler texto de PDFs e imagens.

**Download:** https://github.com/UB-Mannheim/tesseract/wiki

Durante a instalação:
- ✅ Marque: **"Additional language data"**
- ✅ Selecione: **"Portuguese"** na lista
- ✅ Deixe o caminho padrão: `C:\Program Files\Tesseract-OCR`

### **2️⃣ Instale o Poppler**

Necessário para processar PDFs.

1. **Download:** https://github.com/oschwartz10612/poppler-windows/releases/
   - Baixe o arquivo `Release-XX.XX.X-0.zip` (mais recente)

2. **Extraia** para: `C:\Program Files\poppler`

3. **Adicione ao PATH:**
   - Pressione `Win + R`, digite `sysdm.cpl`, Enter
   - Aba "Avançado" → "Variáveis de Ambiente"
   - Em "Variáveis do sistema", selecione `Path` → "Editar"
   - Clique "Novo" e adicione: `C:\Program Files\poppler\Library\bin`
   - OK em tudo
   - **Reinicie o computador**

### **3️⃣ Execute o Files-On**

- Clique duas vezes em `Files-On.exe`
- Pronto! 🎉

---

## 🆘 **Problemas?**

### Erro: "Tesseract não encontrado"
- Reinstale o Tesseract
- Certifique-se que está em `C:\Program Files\Tesseract-OCR`

### Erro: "Poppler não encontrado"
- Verifique se está em `C:\Program Files\poppler\Library\bin`
- Verifique se adicionou ao PATH corretamente
- Reinicie o computador

### App não abre
- Desabilite temporariamente o antivírus
- Clique direito → "Executar como Administrador"

---

## 📞 **Suporte**

Para mais ajuda, entre em contato com o desenvolvedor.
