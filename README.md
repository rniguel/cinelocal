# 🎬 CineLocal - Home Theater & Streaming Doméstico

Bem-vindo ao **CineLocal**, uma central de streaming multimídia de alta performance feita em Python e Web moderna para você reproduzir sua coleção local de filmes e séries no seu computador, celular ou Smart TV com uma experiência visual cinematográfica estilo Netflix.

---

## ⚡ Início Rápido (Executáveis na Raiz)

| Arquivo | Descrição |
|---|---|
| **`Abrir CineLocal.bat`** | Inicia a interface web diretamente no seu navegador padrão. |
| **`Iniciar Servidor (TV e Celular).bat`** | Inicia o servidor HTTP local na sua rede Wi-Fi/Ethernet para você assistir na Smart TV, celular ou tablet pelo endereço IP local (ex: `http://192.168.x.x:8000`). |
| **`Atualizar Catalogo.bat`** | Escaneia sua pasta `media/`, detecta novos filmes/séries, atualiza resoluções, áudio (Dublado/Legendado), legendas e capas automaticamente. |

---

## 🚀 Principais Funcionalidades

### 1. 🍿 Catálogo Dinâmico & Busca Instantânea
* **Busca em Tempo Real:** Pesquisa instantânea por título, ano, franquia ou gênero no cabeçalho.
* **Filtros Rápidos:** Navegação ágil por abas: *Todos*, *Franquias & Sagas*, *Filmes Avulsos* e *4K Ultra HD*.
* **Hero Banner Dinâmico:** Destaque no topo com o filme do momento, backdrop cinematográfico e botões de reprodução rápida.
* **Tela de Onboarding Integrada:** Caso a pasta de filmes ainda esteja vazia, uma interface interativa de boas-vindas guia o usuário passo a passo.

### 2. 📺 Suporte Completo a Séries de TV
* Detecção automática de temporadas (`Season 01`, `Season 02`) e episódios (`S01E01`, `S01E02`).
* Modal dedicado para séries com seletor de temporadas e lista de episódios individuais.

### 3. 🔊 Player Web Cinematográfico
* **Controle de Volume com Boost de 200%:** Amplificador dinâmico via Web Audio API para filmes com áudio baixo, permitindo dobrar o volume além do limite convencional de 100%.
* **Legendas Inteligentes:** Renderização de legendas `.srt` externas ou embutidas com suporte a busca de frases dentro do filme e salto temporal.
* **Atalhos de Teclado:**
  * `Espaço` / `K`: Pausar / Reproduzir
  * `Setas Esquerda / Direita` ou `J / L`: Voltar / Avançar 10 segundos
  * `Setas Cima / Baixo`: Aumentar / Diminuir volume
  * `F`: Alternar tela cheia (Fullscreen)
  * `M`: Silenciar (Mute)

### 4. ⚡ Módulo Universo Marvel (MCU) & Rastreador Canônico (Opcional)
* Se você adicionar produções da Marvel Studios em `media/filmes/Marvel/`, o CineLocal ativa automaticamente:
  * **Carrossel Cronológico do MCU:** Filmes e séries ordenados pela cronologia narrativa canônica.
  * **Guia & Rastreador (66 Títulos):** Modal interativo que rastreia os 66 lançamentos oficiais da Marvel Studios até 2026, indicando o que já está disponível na sua coleção e o que falta baixar.

### 5. 🛠️ Recursos Opcionais & Detecção Automática
* **FFmpeg (Opcional):** Utilizado para identificar precisamente faixas de áudio dublado/original e analisar canais de som.
  * *Como obter:* Pode ser baixado em [ffmpeg.org](https://ffmpeg.org/download.html) ou instalado via Windows Terminal: `winget install Gyan.FFmpeg`.
  * Caso não esteja presente, o CineLocal utiliza uma detecção inteligente por nome sem travar.
* **VLC Media Player (Opcional):** Permite abrir arquivos pesados com áudio surround de cinema (Dolby Atmos, TrueHD, DTS 7.1) em 1 clique direto no VLC.
  * *Como obter:* Baixe gratuitamente em [videolan.org/vlc](https://www.videolan.org/vlc/).
  * Se o VLC não estiver instalado, os botões são ocultados automaticamente e toda a reprodução ocorre pelo player web nativo.

---

## 📁 Estrutura de Pastas do Projeto

```text
CineLocal/
├── Abrir CineLocal.bat                # Inicia a interface no navegador
├── Iniciar Servidor (TV e Celular).bat# Inicia o servidor local na rede
├── Atualizar Catalogo.bat             # Atualiza catálogo e metadados
├── README.md                          # Guia completo do projeto
├── GEMINI.md                          # Regras e convenções para assistentes IA
├── docs/                              # Documentações técnicas e aprofundadas
│   ├── ARQUITETURA.md                 # Arquitetura do backend e frontend
│   ├── GUIA_MIDIA.md                  # Padrões de arquivos, codecs e legendas
│   ├── MCU_TIMELINE.md                # Linha do tempo completa dos 66 títulos Marvel
│   └── SCRIPTS_UTILITARIOS.md         # Detalhes dos scripts utilitários
├── app/                               # Código-fonte da aplicação
│   ├── index.html                     # Interface web do CineLocal (SPA)
│   ├── generate_netflix_ui.py         # Gerador mestre da interface HTML/CSS/JS
│   ├── atualizar_catalogo.py          # Scanner de mídia e compilador de catalogo.js
│   ├── metadata_db.py                 # Banco de metadados ricos (sinopses, elenco, links)
│   ├── otimizar_audio_web.py          # Utilitário de conversão de áudio para AAC estéreo
│   ├── servidor.py                    # Servidor local Python com suporte a VLC e streaming
│   ├── catalogo.sample.js             # Modelo inicial do banco de dados JavaScript
│   └── catalogo.js                    # Base de dados compilada localmente (ignorado no Git)
└── media/
    ├── filmes/                        # Coloque aqui seus filmes avulsos e sagas
    └── series/                        # Coloque aqui suas séries organizadas por temporadas
```

---

## 🍿 Como Usar com seus Próprios Filmes

1. **Adicionar Filmes:**
   * Crie uma pasta em `media/filmes/Nome do Filme (Ano)/`.
   * Coloque o vídeo: `Nome do Filme (Ano) [1080p].mp4` (ou `.mkv`, `.avi`, etc.).
   * Opcional: Adicione a imagem da capa como `poster.jpg` (proporção 2:3) e legendas externas `.srt`.

2. **Adicionar Séries:**
   * Crie uma pasta em `media/series/Nome da Serie/`.
   * Crie pastas de temporada: `Season 01/`, `Season 02/`.
   * Coloque os episódios: `Nome da Serie - S01E01.mkv`.
   * Opcional: Coloque `poster.jpg` na pasta da série.

3. **Atualizar e Assistir:**
   * Dê dois cliques em **`Atualizar Catalogo.bat`** (ou rode `python app/atualizar_catalogo.py`).
   * Dê dois cliques em **`Abrir CineLocal.bat`** (ou rode `python run.py`).
   * Aproveite sua sessão de cinema particular!

---

*Desenvolvido com foco em velocidade, autonomia e máxima fidelidade de áudio e vídeo.*
