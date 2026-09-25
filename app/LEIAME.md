# 🎬 CineLocal - Home Theater & Streaming Local (Estilo Netflix)

Toda a sua coleção de filmes e séries organizada em uma aplicação moderna e limpa, para assistir no Computador, na Smart TV ou no celular.

---

## 📁 Nova Arquitetura de Pastas

```text
CineLocal/ (ou raiz D:\Filmes)
├── app/                              # Código da aplicação, servidor e ferramentas
│   ├── bin/                          # FFmpeg para streaming e áudio
│   ├── vlc/                          # VLC Portable integrado
│   ├── index.html                    # Interface moderna estilo Netflix / Prime Video
│   ├── catalogo.js                   # Banco de dados indexado
│   ├── servidor.py                   # Servidor de streaming HTTP 206
│   ├── atualizar_catalogo.bat / .py  # Indexador automático de filmes e séries
│   └── otimizar_audio_web.bat / .py  # Injetor de áudio compatível para navegador
├── media/
│   ├── filmes/                       # Todos os filmes avulsos e sagas (Marvel, Batman, etc.)
│   └── series/                       # Séries organizadas por temporadas (The Bear, etc.)
├── Abrir CineLocal.bat               # 1 clique para iniciar no PC
├── Iniciar Servidor (TV e Celular).bat# 1 clique para gerar o link da TV/Celular
└── run.py                            # Inicializador universal via Python
```

---

## 🚀 Como Usar

### 💻 No Computador
- Dê dois cliques em **`Abrir CineLocal.bat`** na raiz.
- O catálogo abrirá no seu navegador com layout Netflix, Hero Banner, trilhos por categorias, busca instantânea e suporte a 1 clique para abrir qualquer título no VLC Portable.

### 📺 Na Smart TV, Celular ou Tablet (Mesma Rede Wi-Fi)
1. Dê dois cliques em **`Iniciar Servidor (TV e Celular).bat`** na raiz.
2. O terminal exibirá o endereço IP local (exemplo: `http://192.168.18.5:8000`).
3. Digite esse endereço no navegador da sua TV ou smartphone e aproveite!

---

## ⚡ Novas Funcionalidades

1. **Universo Marvel em Ordem Cronológica:**
   - 12 filmes do MCU indexados na sequência canônica exata dos acontecimentos (do *01 - Capitão América - O Primeiro Vingador* até *12 - Quarteto Fantástico*).
2. **Suporte Completo a Séries (The Bear):**
   - No catálogo e na Home, a série aparece como um card único elegante.
   - Ao clicar, abre a **Modal da Série** com abas de temporada e lista de episódios para dar Play direto ou abrir no VLC.
3. **Navegação por Abas:**
   - **Início:** Hero Banner cinematográfico + Trilhos horizontais (Adicionados Recentemente, Séries, Marvel MCU, Grandes Franquias e Filmes).
   - **Filmes:** Grade completa de longas-metragens com filtros (4K, 1080p, Franquias, Avulsos).
   - **Séries:** Grade exclusiva de séries.
4. **Capas Oficiais em Alta Definição:**
   - 100% dos filmes e séries agora possuem `poster.jpg` oficial em alta resolução baixado do TMDb.

---

## ⌨️ Atalhos de Teclado no Player
- <kbd>Espaço</kbd> ou <kbd>K</kbd>: Play / Pause
- <kbd>→</kbd> / <kbd>←</kbd>: Avançar / Voltar 10 segundos
- <kbd>F</kbd>: Tela Cheia
- <kbd>C</kbd>: Ligar / Alternar Legenda
- <kbd>N</kbd>: Próximo Episódio (em séries)
- <kbd>V</kbd>: Abrir no VLC Portable (Áudio 5.1 surround)
- <kbd>Esc</kbd>: Fechar Player / Fechar Modal da Série

---

## 🔄 Como Adicionar Novos Títulos
- **Filmes:** Coloque em `media/filmes/Nome do Filme (Ano)/` com `poster.jpg`.
- **Séries:** Coloque em `media/series/Nome da Série/Season 01/Nome - S01E01.mkv` com `poster.jpg`.
- Dê dois cliques em **`app\atualizar_catalogo.bat`** e o catálogo estará pronto instantaneamente!
