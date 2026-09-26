# 🎬 CineLocal - Home Theater & Streaming Doméstico

Bem-vindo ao **CineLocal**, uma central de streaming multimídia de alta performance feita em Python e Web moderna para você reproduzir sua coleção local de filmes e séries no seu computador, celular ou Smart TV com uma experiência visual cinematográfica estilo Netflix.

---

## ⚡ Início Rápido (Executáveis na Raiz)

| Arquivo | Descrição |
|---|---|
| **`Abrir CineLocal.bat`** | Inicia a interface web diretamente no seu navegador padrão. |
| **`Iniciar Servidor (TV e Celular).bat`** | Inicia o servidor HTTP local na sua rede Wi-Fi/Ethernet para você assistir na Smart TV, celular ou tablet pelo endereço IP local (ex: `http://192.168.x.x:8000`). |
| **`Atualizar Catalogo.bat`** | Escaneia sua pasta `media/`, detecta novos filmes/séries, atualiza resoluções, áudio (Dublado/Legendado), legendas e capas automaticamente ordenando por data de adição real. |
| **`Buscar Metadados (TMDb).bat`** | Utilitário desacoplado e opcional para buscar sinopses em pt-BR, notas e pôsteres oficiais no The Movie Database sem alterar seus vídeos. |
| **`Otimizar Audio Web.bat`** | Adiciona faixa estéreo AAC sem recodificar o vídeo para reprodução com áudio perfeito em qualquer navegador web. |

---

## 🚀 Principais Funcionalidades

### 1. 🍿 Catálogo Dinâmico & Descoberta
* **⭐ Minha Lista (Favoritos):** Salve filmes e séries favoritos com um clique no card ou na ficha técnica. Conta com carrossel exclusivo no Início e filtro dedicado na aba de Filmes.
* **🔍 Busca Global Inteligente:** Pesquisa instantânea por título, atores (`cast`), diretores/criadores (`director`/`creator`), gêneros e termos da sinopse. Pressione `/` no teclado para focar a barra de pesquisa a qualquer momento.
* **🎬 Trailers Oficiais Integrados:** Assista à prévia do trailer oficial em alta definição diretamente do YouTube antes de iniciar a sessão.
* **Continuar Assistindo Sincronizado:** Salva o ponto exato da reprodução e sincroniza automaticamente entre computadores, celulares e Smart TVs na mesma rede.
* **Filtros Avançados:** Filtre instantaneamente por **Gênero** (Ação, Drama, Ficção...), **Ano / Década**, **Favoritos** e **Não Assistidos**.
* **🎲 Surpreenda-me (Roleta de Filmes):** Sorteie um filme do catálogo para aqueles momentos de indecisão.
* **Adicionados Recentemente Precisos:** Ordenação baseada na data real de gravação/modificação dos arquivos no disco.
* **Marcação de Assistido:** Marque filmes e séries como assistidos com um clique para manter sua biblioteca organizada.
* **Tela de Onboarding Integrada:** Caso a pasta de filmes ainda esteja vazia, uma interface interativa de boas-vindas guia o usuário passo a passo.

### 2. 📺 Smart TV & Conexão Rápida
* **📱 Controle Remoto Virtual para Celular (`/remote`):** Transforme qualquer celular em um controle touch sem latência. Acesse `http://<ip>:8000/remote` ou aponte a câmera para o QR Code da aplicação.
  * D-Pad tátil com vibração (haptic feedback) para navegar menus da Smart TV sem mouse.
  * Comandos de Play/Pause, Seek (-10s / +10s), Volume (- / + / Mute), Fullscreen e Voltar.
  * Ajuste de sincronia de legendas em tempo real direto da palma da mão.
* **Navegação D-Pad Nativa para Smart TV:** Suporte total às setas do controle físico da TV (`↑`, `↓`, `←`, `→`) e `Enter / OK` para focar cards e botões.
* **Conexão via QR Code:** Abra a câmera do celular ou digite o link direto na TV para carregar o CineLocal ou abrir o controle remoto instantaneamente.
* **Detecção Automática de IP Local:** Mostra o IP do computador na rede local sem configurações complexas.

### 3. 🔊 Player Web Cinematográfico Avançado
* **🎵 Seletor de Faixas de Áudio:** Identifica trilhas embutidas (Dublado / Legendado / Original) e permite alternar faixas diretamente no menu de áudio do player.
* **Clique na Tela para Play/Pause:** Clique em qualquer ponto do vídeo para pausar ou reproduzir, com animação central de feedback estilo YouTube.
* **Controles Inteligentes em Tela Cheia:** Os controles surgem instantaneamente ao mover o mouse e permanecem visíveis durante o pause.
* **Picture-in-Picture (PiP):** Assista em janela flutuante enquanto utiliza outros programas no computador.
* **Velocidade de Reprodução Dinâmica:** Alterne entre 0.75x, 1.0x, 1.25x, 1.5x e 2.0x com os atalhos `[` e `]`.
* **Próximo Episódio Automático:** Contagem regressiva nos últimos 20 segundos de um episódio para iniciar o próximo sem esforço.
* **Super Booster de Volume (até 300%):** Amplificador dinâmico via Web Audio API para filmes com áudio baixo.
* **Legendas Inteligentes:** Renderização de legendas `.srt` com ajuste fino de sincronia (`G` e `H`) e tamanhos personalizáveis.
* **Atalhos de Teclado:**
  * `/`: Focar na barra de busca global
  * `Espaço` / `K`: Pausar / Reproduzir
  * `Setas Esquerda / Direita`: Voltar / Avançar 10 segundos
  * `Setas Cima / Baixo`: Volume (0% a 300%)
  * `F`: Alternar tela cheia (Fullscreen)
  * `M`: Silenciar (Mute)
  * `P`: Janela Flutuante (Picture-in-Picture)
  * `[` / `]`: Diminuir / Aumentar velocidade
  * `N`: Próximo episódio
  * `V`: Abrir no VLC Media Player (Áudio 5.1/7.1)
  * `C`: Abrir seletor de legendas
  * `G` / `H`: Ajustar sincronia da legenda (-0.1s / +0.1s)
  * `Esc`: Fechar player ou modais

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
├── Buscar Metadados (TMDb).bat        # Enriquecedor de metadados e pôsteres via TMDb
├── Otimizar Audio Web.bat             # Converte áudio de vídeos incompatíveis
├── README.md                          # Guia completo do projeto
├── GEMINI.md                          # Regras e convenções para assistentes IA
├── docs/                              # Documentações técnicas e aprofundadas
│   ├── ARQUITETURA.md                 # Arquitetura do backend e frontend
│   ├── GUIA_MIDIA.md                  # Padrões de arquivos, codecs e legendas
│   ├── MCU_TIMELINE.md                # Linha do tempo completa dos 66 títulos Marvel
│   └── SCRIPTS_UTILITARIOS.md         # Detalhes dos scripts utilitários
├── app/                               # Código-fonte da aplicação
│   ├── index.html                     # Interface web do CineLocal (SPA)
│   ├── remote.html                    # Controle remoto mobile tátil (SSE em tempo real)
│   ├── generate_netflix_ui.py         # Gerador mestre da interface HTML/CSS/JS
│   ├── atualizar_catalogo.py          # Scanner de mídia e compilador de catalogo.js
│   ├── buscar_metadados_tmdb.py       # Utilitário desacoplado de consulta à API TMDb
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
