# 🎬 CineLocal - Home Theater, Streaming Doméstico & Central Multi-Torrent

<p align="center">
  <img src="app/icon-192.png" alt="CineLocal Logo" width="110" />
</p>

<p align="center">
  <strong>Uma central multimídia de alta performance inspirada na interface Netflix e Stremio para reproduzir sua coleção local e torrents em 4K/HDR no PC, Celular e Smart TV.</strong>
</p>

<p align="center">
  <a href="#-início-rápido-1-clique"><img src="https://img.shields.io/badge/Plataforma-Windows%20%7C%20Linux%20%7C%20macOS-blue?style=flat-square" alt="Multiplataforma" /></a>
  <a href="#-principais-funcionalidades"><img src="https://img.shields.io/badge/Tecnologias-Python%20%7C%20Node.js%20%7C%20WebTorrent%20%7C%20FFmpeg-success?style=flat-square" alt="Tecnologias" /></a>
  <a href="docs/ARQUITETURA.md"><img src="https://img.shields.io/badge/Arquitetura-Local--First%20%7C%20HTTP%20206%20%7C%20PWA-orange?style=flat-square" alt="Arquitetura" /></a>
  <a href="CONTRIBUTING.md"><img src="https://img.shields.io/badge/Git%20Flow-develop%20%E2%86%92%20main-red?style=flat-square" alt="Git Flow" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/Licen%C3%A7a-MIT-green?style=flat-square" alt="Licença" /></a>
</p>

---

## ⚡ Início Rápido (1-Clique)

O **CineLocal** conta com scripts prontos para uso imediato na raiz do projeto. Não é necessário configurar portas nem instalar bancos de dados complexos:

### 🪟 No Windows
| Arquivo | Descrição |
|---|---|
| **`Iniciar CineLocal Desktop.bat`** | **Recomendado:** Inicia o aplicativo desktop nativo maximizado (sem barras de navegação do browser e sem avisos de SmartScreen). |
| **`Abrir CineLocal.bat`** | Inicia o servidor local e abre o CineLocal no seu navegador web padrão. |
| **`Iniciar Servidor (TV e Celular).bat`** | Inicia o servidor na sua rede Wi-Fi/Ethernet para assistir em Smart TVs, celulares e tablets pelo IP local (`http://192.168.x.x:8000`). |
| **`Compilar Executavel.bat`** | Compila o executável autônomo `dist/CineLocal/CineLocal.exe` com PyInstaller em 1 clique. |
| **`Atualizar Catalogo.bat`** | Escaneia suas mídias, atualiza capas, resoluções, áudio (Dublado/Legendado) e legendas `.srt`. |

### 🐧 No Linux & 🍎 no macOS
```bash
# Iniciar o CineLocal diretamente no navegador padrão
./run.sh

# Ou para abrir o servidor de rede Wi-Fi para Smart TV / Celular
./"Iniciar Servidor (TV e Celular).sh"
```

### 🐳 Execução via Docker (HomeLabs, NAS e Servidores)
```bash
docker compose up -d
```
Acesse `http://localhost:8000` (ou o IP do seu servidor). Suas mídias são mapeadas em modo seguro somente leitura (`:ro`) e favoritos/progresso são preservados em `./app/data`.

---

## 🚀 Principais Funcionalidades

### 1. ⚡ Central Multi-Torrent & Streaming Sequencial (Estilo Stremio)
* **Reprodução Imediata (Buffer de 2 MB):** Assista a qualquer Magnet Link instantaneamente sem precisar esperar o download de 100% de arquivos de vários gigabytes.
* **🚀 Assistir no VLC (1-Clique):** Reproduza arquivos `.mkv`, 4K, HDR, Dolby Atmos e DTS 7.1 diretamente no VLC Player com decodificação de hardware e legendas sincronizadas.
* **Remux On-the-Fly no Navegador:** Para arquivos `.mkv` ou faixas de áudio surround, o CineLocal faz remux em tempo real via FFmpeg (`-c:v copy -c:a aac`) entregando compatibilidade total para navegadores sem gastar CPU com re-encodificação de vídeo.
* **📥 Fila de Downloads em Tempo Real:** Monitore múltiplos downloads simultâneos com taxa de transferência (MB/s), sementes ativas (seeds), progresso percentual e botões para Reproduzir, Salvar ou Remover.
* **📁 Salvamento Automático na Pasta de Vídeos do SO:** Filmes finalizados são organizados diretamente na pasta padrão do seu sistema:
  * Windows: `C:\Users\<SeuUsuario>\Videos\CineLocal\<Nome do Filme (Ano)>\`
  * Linux: `~/Videos/CineLocal/<Nome do Filme (Ano)>/`
  * macOS: `~/Movies/CineLocal/<Nome do Filme (Ano)>/`

### 2. 📱 Controle Remoto Virtual para Smart TV & Celular (`/remote`)
* **Transforme qualquer smartphone em controle remoto touch:** Acesse `http://<ip-do-pc>:8000/remote` ou aponte a câmera para o QR Code da aplicação.
* **D-Pad Tátil com Vibração (Haptic Feedback):** Navegue pelas capas na tela grande da TV usando o direcional touch do celular com resposta tátil.
* **Sem Latência (< 20ms):** Comunicação baseada em **Server-Sent Events (SSE)** em tempo real.
* **Comandos Completos:** Play/Pause, Seek (+/- 10s), Volume (+/- / Mudo), Tela Cheia, Fechar e ajuste fino de sincronia de legendas (+/- 0.1s).

### 3. 🍿 Player Cinematográfico HTML5 Avançado
* **HTTP 206 Partial Content:** Seek instantâneo na linha do tempo em arquivos 1080p e 4K.
* **Super Booster de Volume (Até 300%):** Amplificador de ganho via Web Audio API para filmes com áudio baixo.
* **Seletor de Faixas de Áudio:** Identifica e permite alternar entre trilhas de áudio embutidas (Dublado / Legendado / Original).
* **Picture-in-Picture (PiP):** Janela flutuante para assistir enquanto usa outros programas.
* **Legendas Inteligentes:** Renderização de `.srt` com limpeza automática de tags indesejadas e ajuste de atraso/avanço em milissegundos.
* **Velocidade Dinâmica:** Alterne de 0.75x a 2.0x instantaneamente.
* **Contagem Regressiva de Próximo Episódio:** Avança automaticamente para o próximo capítulo de séries.

### 4. 📺 Navegação Especial para Smart TV (D-Pad Físico)
* Navegue facilmente com as setas físicas do controle remoto da Smart TV (`↑`, `↓`, `←`, `→` e `OK`).
* Borda pulsante luminosa em vermelho vibrante (*glow* cinemático) e centralização suave no carrossel.

### 5. ⚡ Linha do Tempo Canônica Marvel MCU (67 Produções)
* **Carrossel Cronológico:** Se você tiver filmes da Marvel Studios em `media/filmes/Marvel/`, o CineLocal ativa a ordem canônica do MCU.
* **Rastreador Oficial de Coleção:** Modal interativo que mapeia todas as 67 produções oficiais do Marvel Studios até 2026, destacando o que você já possui e o que falta baixar.

### 6. 🖥️ Aplicativo Desktop Windows Autônomo
* Executável portátil compilado em `dist/CineLocal/CineLocal.exe` (2.5 MB).
* Inicializador dedicado `Iniciar CineLocal Desktop.bat` com bypass automático do Windows SmartScreen.
* Script oficial Inno Setup em `installer/CineLocal.iss` para empacotar em instaladores tradicionais do Windows (`CineLocal-Setup-v2.5.0.exe`).

---

## ⌨️ Atalhos de Teclado no Player

| Tecla | Ação |
|---|---|
| **`/`** | Focar na barra de busca global |
| **`Espaço`** ou **`K`** | Pausar / Reproduzir |
| **`Setas ← / →`** | Voltar / Avançar 10 segundos |
| **`Setas ↑ / ↓`** | Ajustar volume (0% a 300%) |
| **`F`** | Alternar Tela Cheia (Fullscreen) |
| **`M`** | Silenciar / Ativar Som (Mute) |
| **`P`** | Modo Picture-in-Picture (Janela Flutuante) |
| **`[` / `]`** | Diminuir / Aumentar velocidade de reprodução |
| **`V`** | Abrir filme diretamente no VLC Player |
| **`C`** | Abrir menu de seleção de legendas |
| **`G` / `H`** | Ajustar sincronia da legenda (-0.1s / +0.1s) |
| **`N`** | Próximo episódio da série |
| **`Esc`** | Fechar player ou modais abertos |

---

## 📁 Estrutura de Pastas e Mídias

```text
CineLocal/
├── Iniciar CineLocal Desktop.bat      # 🚀 Inicia como app desktop nativo
├── Abrir CineLocal.bat                # Inicia no navegador padrão
├── Iniciar Servidor (TV e Celular).bat# Inicia o servidor local na rede Wi-Fi
├── Compilar Executavel.bat            # Compila o executável .exe via PyInstaller
├── Atualizar Catalogo.bat             # Atualiza catálogo e metadados
├── run.py / run.sh                    # Inicializador multiplataforma
├── build_desktop.py                   # Construtor do executável PyInstaller
├── run_desktop.py                     # Launcher desktop em modo janela
│
├── app/
│   ├── index.html                     # ⭐️ Interface oficial (Fonte da Verdade)
│   ├── remote.html                    # Controle remoto mobile touch (SSE)
│   ├── servidor.py                    # Servidor HTTP 206, SSE e Remuxer FFmpeg
│   ├── atualizar_catalogo.py          # Scanner de mídia e indexador
│   ├── metadata_db.py                 # Banco de metadados ricos (sinopses, elenco)
│   ├── torrent/
│   │   ├── engine.mjs                 # Motor WebTorrent sequencial (Porta 8888)
│   │   └── package.json               # Dependências do motor de torrent
│   └── data/                          # Dados de favoritos e progresso
│
├── docs/                              # 📚 Guias arquiteturais detalhados
│   ├── ARQUITETURA.md                 # Arquitetura técnica e fluxos de dados
│   ├── TORRENT_STREAMING.md           # Guia de torrents e streaming sequencial
│   ├── CONTROLE_REMOTO.md             # Guia do controle remoto SSE para celular
│   ├── GUIA_DESKTOP.md                # Guia de compilação .exe e Inno Setup
│   ├── GUIA_MIDIA.md                  # Padrões de nomenclatura de filmes/séries
│   └── MCU_TIMELINE.md                # Documentação da cronologia Marvel
│
└── media/
    ├── filmes/                        # Filmes avulsos e sagas em disco
    │   └── Vídeos/                    # Link automático com a pasta de Vídeos do SO
    └── series/                        # Séries organizadas por temporadas
```

---

## 🍿 Organizando seus Próprios Filmes

1. **Filmes Avulsos:**
   `media/filmes/Nome do Filme (Ano)/Nome do Filme (Ano) [1080p].mp4`
2. **Franquias e Sagas (Ordem Numérica):**
   `media/filmes/Marvel/01 - Capitão América (2011)/Capitão América (2011) [1080p].mkv`
3. **Séries de TV:**
   `media/series/Nome da Serie/Season 01/Nome da Serie - S01E01.mkv`
4. **Posters e Legendas:**
   * Capas: salve como `poster.jpg` na pasta do filme/série (proporção 2:3).
   * Legendas: arquivos `.srt` na mesma pasta do vídeo (ex: `Nome.srt` ou `Nome.pt.srt`).

---

## 📚 Documentação Técnica Aprofundada

Explore a pasta [`docs/`](docs/) para guias especializados:

* [🏛️ **Arquitetura Geral do Sistema** (`docs/ARQUITETURA.md`)](docs/ARQUITETURA.md) — Diagramas de fluxo, SSE, HTTP 206 e remuxer.
* [⚡ **Streaming de Torrent & Multi-Torrent** (`docs/TORRENT_STREAMING.md`)](docs/TORRENT_STREAMING.md) — Motor sequencial, buffers de 2MB e VLC.
* [📱 **Controle Remoto Touch & Smart TV** (`docs/CONTROLE_REMOTO.md`)](docs/CONTROLE_REMOTO.md) — Pareamento QR Code e D-Pad tátil.
* [🖥️ **Guia do Aplicativo Desktop** (`docs/GUIA_DESKTOP.md`)](docs/GUIA_DESKTOP.md) — Executável `.exe`, scripts `.bat` e Inno Setup.
* [🗂️ **Padrões de Nomenclatura de Mídia** (`docs/GUIA_MIDIA.md`)](docs/GUIA_MIDIA.md) — Diretrizes para pastas e metadados.
* [⚡ **Linha do Tempo Canônica Marvel** (`docs/MCU_TIMELINE.md`)](docs/MCU_TIMELINE.md) — Mapeamento das 67 produções do MCU.

---

## 🤝 Como Contribuir & Git Flow

Adotamos a estratégia baseada em **Git Flow**:

```text
main       ●─────────────────────────────────────● (Releases Estáveis)
            \                                   /
develop      ●─────────●──────────────●────────● (Integração & Desenvolvimento)
                        \            /
feature/fix              ●──────────● (Sua Branch de Trabalho)
```

1. Clone o repositório e crie sua branch a partir de `develop`:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/minha-melhoria
   ```
2. Respeite as regras do CineLocal:
   * **Interface Web:** Alterações de UI devem ser aplicadas em `app/index.html` (Fonte da Verdade) e validadas com `python app/generate_netflix_ui.py`.
   * **Preservação de Mídia:** Nunca adicione rotinas destrutivas que excluam vídeos.
   * **Codificação:** Mantenha os arquivos em `UTF-8`.
3. Faça commits semânticos:
   ```bash
   git commit -m "feat(torrent): adicionar suporte a priorizacao customizada"
   ```
4. Abra um Pull Request apontando para a branch `develop`.

Para diretrizes completas de contribuição, consulte o [**CONTRIBUTING.md**](CONTRIBUTING.md).

---

<p align="center">
  <em>Desenvolvido com foco em velocidade, autonomia, design cinemático e máxima fidelidade de áudio e vídeo.</em>
</p>
