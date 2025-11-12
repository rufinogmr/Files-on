# 📦 Como Distribuir o Files-On

## 🎯 **Opção 1: Instalador Super Simples (RECOMENDADO)**

### **Você faz (UMA VEZ):**

```batch
# 1. Crie o executável
build.bat

# 2. Pronto! Agora você tem tudo pronto
```

### **Passe pro seu pai (3 arquivos):**

Crie uma pasta `Files-On-Instalador` com estes arquivos:

```
📁 Files-On-Instalador/
   ├── INSTALAR-DUPLO-CLIQUE.bat  ⭐ (este é o instalador)
   ├── dist/Files-On.exe           (o executável)
   └── LEIA-ME.txt                 (instruções)
```

### **Seu pai faz:**

1. **Clica DIREITO** em `INSTALAR-DUPLO-CLIQUE.bat`
2. Escolhe **"Executar como administrador"**
3. Segue as instruções na tela
4. **Reinicia o PC**
5. **Clica no ícone** do Files-On na Área de Trabalho

**PRONTO!** ✅

---

## 🎁 **Opção 2: Instalador Profissional (como Chrome/WhatsApp)**

Se quiser criar um `setup.exe` profissional:

### **1. Instale o Inno Setup:**
- Baixe: https://jrsoftware.org/isdl.php
- Instale normalmente

### **2. Crie o executável:**
```batch
build.bat
```

### **3. Compile o instalador:**
- Abra o Inno Setup Compiler
- File → Open → Selecione `installer.iss`
- Build → Compile
- Pronto! Vai criar `installer/Files-On-Instalador.exe`

### **Seu pai faz:**
1. **Duplo clique** em `Files-On-Instalador.exe`
2. Next, Next, Next... (como qualquer programa)
3. Finish
4. **Pronto!** Ícone aparece na Área de Trabalho

---

## ⚠️ **Importante:**

O instalador vai:
- ✅ Detectar se Tesseract está instalado
- ✅ Detectar se Poppler está instalado
- ✅ Abrir páginas de download se necessário
- ✅ Criar atalhos automaticamente
- ✅ Adicionar tudo ao PATH

Se Tesseract ou Poppler não estiverem instalados, o instalador vai pausar e pedir pra instalar (abre a página automaticamente).

---

## 💡 **Dica:**

Para **ZERO configuração**, você pode:
1. Instalar Tesseract e Poppler no seu PC
2. Criar o executável com build.bat
3. Copiar também as DLLs do Tesseract e Poppler
4. Usar PyInstaller para incluir tudo (executável portável)

Quer que eu crie essa versão portável? 🚀
