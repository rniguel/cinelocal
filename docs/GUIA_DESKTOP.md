# 🖥️ Guia do Aplicativo Desktop Autônomo & Compilação

O **CineLocal** pode ser executado como um aplicativo desktop nativo sem barras de navegação do browser, proporcionando uma experiência de cinema limpa e autônoma no Windows, Linux e macOS.

---

## ⚡ 1. Inicialização Rápida no Windows (1 Clique)

Na pasta raiz do CineLocal, disponibilizamos scripts prontos para uso:

| Arquivo | Finalidade |
|---|---|
| **`Iniciar CineLocal Desktop.bat`** | **Recomendado para o dia a dia.** Inicia o CineLocal em modo aplicativo nativo maximizado, sem avisos de segurança do Windows SmartScreen. |
| **`Compilar Executavel.bat`** | Compila o executável autônomo `dist/CineLocal/CineLocal.exe` utilizando PyInstaller em 1 clique. |
| **`Abrir CineLocal.bat`** | Inicia o servidor e abre o CineLocal no navegador padrão. |

---

## 📦 2. Executável Compilado (`CineLocal.exe`)

O executável portátil encontra-se em:
```text
dist/CineLocal/CineLocal.exe
```

### 🛡️ Aviso do Windows SmartScreen ("Fornecedor Desconhecido")
Como o executável é gerado localmente na máquina do usuário e não possui um certificado digital comercial da Microsoft (que exige taxas anuais de empresas registradas), o Windows Defender SmartScreen pode exibir um aviso azul na primeira inicialização:

1. Clique em **"Mais informações"**.
2. Clique no botão **"Executar assim mesmo"**.
3. O aplicativo abrirá normalmente. Isso é necessário apenas uma única vez.
> 💡 **Dica:** O script **`Iniciar CineLocal Desktop.bat`** contorna automaticamente esse bloqueio através do PowerShell `Unblock-File`, abrindo o aplicativo sem nenhuma interrupção.

---

## 🔨 3. Compilando do Código Fonte com PyInstaller

Caso queira recompilar o `.exe` após fazer alterações no código:

```bash
# Executar o script de compilação oficial
python build_desktop.py
```

### O que o `build_desktop.py` faz:
1. Detecta o ambiente Python e instala o `pyinstaller` caso não esteja presente.
2. Gera o arquivo de ícone `app/icon.ico` a partir da imagem oficial `app/icon-192.png`.
3. Configura a especificação com:
   - Modo janela (`console=False`) sem terminal preto aparente.
   - Otimização de dependências ocultas (`hiddenimports` com módulos do servidor e banco de metadados).
   - Diretório temporário de compilação no drive `C:` com dezenas de gigabytes livres (`--workpath`).
4. Empacota todas as mídias, HTML, CSS, JavaScript e ícones na pasta `dist/CineLocal/`.

---

## 💿 4. Gerando um Instalador com Inno Setup

Para distribuir o CineLocal como um instalador clássico do Windows (`CineLocal-Setup-v2.5.exe`):

1. Baixe e instale o [Inno Setup 6](https://jrsoftware.org/isdl.php) (software gratuito e de código aberto).
2. Abra o arquivo de script do instalador:
   ```text
   installer/CineLocal.iss
   ```
3. Pressione **`F9`** (ou clique no menu **Build > Compile**).
4. O instalador será gerado em:
   ```text
   dist/installer/CineLocal-Setup-v2.5.0.exe
   ```
   Ele adicionará atalhos na Área de Trabalho e no Menu Iniciar do Windows, associando ícones e configurando a desinstalação automática.
