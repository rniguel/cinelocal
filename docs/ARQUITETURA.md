# 🏛️ Arquitetura do Sistema CineLocal

O **CineLocal** é projetado como uma aplicação web híbrida de alto desempenho para redes locais, combinando um frontend moderno e reativo (*Single Page Application*) com um servidor Python leve e utilitários de mídia via FFmpeg.

---

## 🏗️ Visão Geral da Arquitetura

```text
[Arquivos Locais em Disco]
        │
        ├── media/filmes & media/series
        │       │
        │       ▼
  [atualizar_catalogo.py] ◄──── [metadata_db.py] (Sinopses, Elenco, TMDb)
        │                 ◄──── [.audio_cache.json] (Cache inteligente mtime)
        ▼
   [catalogo.js]
        │
        ▼
   [index.html] (Frontend SPA / Web Audio 300% / D-Pad TV / Trailers / VLC)
        ▲               ▲
        │               │ SSE Events & Actions
        ▼               ▼
   [servidor.py] ◄──► [remote.html] (Controle Remoto Touch no Celular)
        │
        ├──► [app/data/user_state.json] (Progresso e Favoritos Compartilhados)
        └──► [VLC Media Player (vlc.exe)]
```

---

## 🖥️ 1. Frontend (`app/index.html` - Fonte da Verdade)

* **Tecnologia:** HTML5 Semântico, CSS Moderno com Variáveis Customizadas, e JavaScript Vanilla puro (sem dependências de frameworks pesados para garantir carregamento instantâneo de milissegundos). A partir da **Issue #8**, o arquivo `app/index.html` é a única fonte da verdade oficial da UI, eliminando o acoplamento com strings de código embutidas.
* **Estrutura de Componentes:**
  * **Header:** Barra de navegação com marca, chips de visualização (*Home*, *Filmes*, *Séries*), atalhos para *Surpreenda-me* (🎲 Roleta), *📱 Controle* (Acesso rápido ao controle remoto virtual), *TV / Celular* (📱 QR Code) e campo de busca global inteligente (atalho `/`).
  * **Hero Banner:** Destaque visual randômico ou curado com imagem de alta resolução, metadados completos e botões de reprodução rápida, trailer e adicionar à lista.
  * **Carrosséis Horizontais com Suporte a Touch e Botões:**
    * *⭐ Minha Lista* (Carrossel dinâmico dos títulos favoritados pelo usuário)
    * *⏱️ Continuar Assistindo* (Itens em andamento com barra de progresso individual e tempo restante, sincronizados com o servidor)
    * *🔥 Adicionados Recentemente* (Ordenados pelo timestamp de modificação real `addedAt`)
    * *📺 Séries & Temporadas*
    * *⚡ Universo Marvel (Ordem Cronológica do MCU)* com Card de Destaque Interativo
    * *🏆 Grandes Franquias & Sagas Épicas*
    * *🎬 Catálogo Geral de Longas-Metragens*
  * **Filtros do Catálogo de Filmes:**
    * Gênero dinâmico (Ação, Drama, Ficção, etc.)
    * Ano / Décadas (2020+, 2010s, 2000s, Clássicos)
    * Status de visualização (*⭐ Favoritos* e *Não Assistidos*)
  * **Player Cinematográfico Integrado:**
    * Implementado sobre a tag `<video>` do HTML5.
    * **Controles Inteligentes:** Ocultação automática após inatividade durante reprodução e exibição permanente no pause.
    * **Clique na Tela:** Pausa/reproduz clicando em qualquer ponto da tela, com pulso visual centralizado estilo YouTube.
    * **Seletor de Faixas de Áudio:** Consulta `/api/audio_info` e permite selecionar trilhas embutidas (Dublado, Legendado, Original).
    * **Picture-in-Picture (PiP):** Janela flutuante nativa do navegador (`document.pictureInPictureElement`).
    * **Velocidade Dinâmica:** Taxas de 0.75x a 2.0x configuráveis por botão e atalhos de teclado (`[` e `]`).
    * **Contagem de Próximo Episódio:** Toast flutuante nos últimos 20 segundos de um episódio para avançar automaticamente.
    * **Persistência Centralizada:** Salva o ponto exato da reprodução no servidor (`/api/progress`) e no `localStorage` como fallback.
    * **Nó de Áudio Web:** `AudioContext` + `GainNode` permitindo amplificação de volume de até 300%.
  * **Navegação Smart TV & D-Pad:**
    * Motor de foco espacial para setas do controle remoto (`↑`, `↓`, `←`, `→`) e `Enter / OK`.
    * Destaque com brilho luminoso (`:focus-visible` e `.tv-focused`).
  * **Modais Reativos:**
    * `#movieDetailsModal`: Ficha completa com sinopse, elenco, botão de continuar assistindo, favoritar, trailer oficial, links TMDb/IMDb e opções de reprodução.
    * `#seriesModal`: Seletor de temporadas e episódios com botão de favoritar, trailer e marcação de assistido.
    * `#trailerModal`: Modal escuro dedicado com reprodução em alta definição do trailer oficial via YouTube.
    * `#surpriseModal`: Roleta aleatória que sorteia produções bem avaliadas do acervo.
    * `#qrModal`: Exibe QR Code com abas para assistir na TV ou abrir o controle remoto no celular.
    * `#mcuTrackerModal`: Linha do tempo de 67 produções da Marvel, monitoramento de coleção e filtros dinâmicos.

---

## 📱 2. Controle Remoto Mobile Touch (`app/remote.html`)

* **Tecnologia:** Interface web touch ultraleve com design dark cinemático.
* **Recursos:**
  * **D-Pad Touch Intuitivo:** Botões circulares para Cima, Baixo, Esquerda, Direita e OK central.
  * **Eventos `pointerdown`:** Disparo instantâneo sem o delay padrão de 300ms de navegadores móveis.
  * **Haptic Feedback:** Vibra suavemente a cada toque em aparelhos compatíveis (`navigator.vibrate(25)`).
  * **Atalhos Dedicados:** Play/Pause, Seek (+/- 10s), Volume (+/- / Mute), Sincronia de legendas (+/- 0.1s), Tela Cheia e Voltar.
  * **Comunicação em Tempo Real:** Conecta-se ao `RemoteControllerHub` do servidor via Server-Sent Events (SSE) com latência imperceptível (< 20ms).

---

## ⚙️ 3. Backend & Servidor Local (`app/servidor.py`)

* **Tecnologia:** Python nativo utilizando `http.server.ThreadingHTTPServer` para atender múltiplas conexões simultâneas de computadores, Smart TVs e celulares.
* **Recursos Especiais do Servidor:**
  * **HTTP Range Requests (Bytes 206 Partial Content):** Permite navegação rápida na barra de tempo do vídeo (*seek*) sem necessidade de baixar o arquivo inteiro.
  * **Hub de Controle Remoto (`RemoteControllerHub`):**
    * `GET /api/remote/events`: Stream via Server-Sent Events (SSE) mantido aberto pelo player da TV/PC.
    * `POST /api/remote/action`: Recebe comandos do celular e despacha para as filas de eventos dos clientes conectados.
    * `GET /remote` ou `/controle`: Redireciona diretamente para `app/remote.html`.
  * **Sincronização de Estado Multi-Dispositivos:**
    * `GET /api/user_state`: Carrega o progresso de reprodução e a lista de favoritos unificada.
    * `POST /api/progress`: Atualiza o tempo assistido de filmes ou episódios de séries em `app/data/user_state.json`.
    * `POST /api/favorite/toggle`: Alterna o estado de favorito de qualquer título e persiste no servidor.
  * **Análise de Faixas de Áudio (`GET /api/audio_info`):** Executa o `ffprobe` para inspecionar trilhas embutidas no contêiner de vídeo e retorna títulos e canais em JSON.
  * **Endpoint `/api/capabilities`:** Informa se o VLC e FFmpeg estão disponíveis, além de expor o IP da rede local (`localIp`) e URL completa (`localUrl`) para o modal de conexão QR Code.
  * **Endpoint `/api/open_vlc`:** Recebe requisições da interface web e executa o VLC Media Player nativo no Windows de forma assíncrona e em background, priorizando caminhos padrão e portáteis.
  * **Detecção Automática de IP Local:** Descobre e imprime no terminal o IP da máquina na rede Wi-Fi/Ethernet (ex: `http://192.168.1.15:8000`), gerando comodidade para quem acessa via Smart TV ou celular.

---

## ⚡ 4. Compilador de Mídia (`app/atualizar_catalogo.py`)

* **Escaneamento Automatizado:**
  * Percorre recursivamente `media/filmes` e `media/series`.
  * Detecta resoluções no nome do arquivo (`2160p`, `4K`, `1080p`, `720p`).
  * Associa pastas de franquia e numerações de sequência.
  * Extrai o timestamp de modificação (`addedAt`) para ordenação real de adições recentes.
* **Cache Inteligente de Áudio (`.audio_cache.json`):**
  * Salva o timestamp (`mtime`) de cada arquivo de vídeo já analisado.
  * Quando um filme ou série não foi alterado, o probe é recuperado instantaneamente da memória sem gastar CPU com o FFmpeg.
  * Se um arquivo for substituído ou adicionado, o sistema detecta a alteração e atualiza apenas a mídia modificada.
* **Higienização de Legendas:**
  * Lê arquivos `.srt` em múltiplas codificações (`utf-8`, `utf-8-sig`, `cp1252`, `latin-1`).
  * Remove tags indesejadas de fontes (`<font color="...">`, `{y:i}`, etc.), garantindo sincronismo e exibição límpida.
* **Geração de Saída:**
  * Compila `catalogo.js` contendo `window.CATALOGO`, `window.CATALOGO_FILMES`, `window.CATALOGO_SERIES` e `window.LEGENDAS_DB`.

---

## 🌐 5. Enriquecedor de Metadados TMDb (`app/buscar_metadados_tmdb.py`)

* **Operação Desacoplada e Opcional:**
  * Não interfere no funcionamento offline padrão do CineLocal.
  * Realiza consultas via API v3 do TMDb em português brasileiro (pt-BR).
  * Faz download de pôsteres oficiais (`poster.jpg`) somente nas pastas que não tiverem imagem.
  * **Preservação de Mídia:** Nunca altera, move ou renomeia os arquivos de vídeo.

---

## 🚀 6. Módulos em Expansão (Roadmap de Arquitetura)

### A. Web Media Manager & Local-First Cloud App (Issue #15)
* **Objetivo:** Permitir publicar o CineLocal na nuvem (Vercel, Netlify, GitHub Pages) como uma SPA moderna e permitir que qualquer usuário conecte e reproduza suas pastas de filmes locais diretamente pelo navegador.
* **Componentes:**
  * **File System Access API (`showDirectoryPicker`):** Leitura de diretórios e arquivos de mídia locais com permissão nativa do navegador.
  * **Blob Streaming (`URL.createObjectURL`):** Reprodução instantânea de vídeos locais no player HTML5 sem consumir tráfego de internet ou custos de servidor.
  * **IndexedDB Persistence:** Armazenamento seguro do handle da pasta e do cache de metadados para carregamento instantâneo em visitas recorrentes.
  * **Organizador em Disco:** Com permissão de escrita, cria pastas no padrão canônico, faz download de posters oficiais do TMDb e move/organiza mídias no próprio disco do usuário.
  * **Modo Dual (Híbrido):** Funciona tanto como Web App online estático quanto integrado ao servidor local Python (`servidor.py`).

### B. Torrent Streaming Engine (Reprodução Direta de Magnet Links - Issue #16)
* **Objetivo:** Reprodução instantânea de torrents no player do CineLocal estilo Stremio.
* **Componentes:**
  * Motor BitTorrent sequencial (`torrent-stream` / `libtorrent`) com janela deslizante de priorização de peças (cabeçalho, índice e agulha de reprodução).
  * Servidor de stream HTTP local suportando `Range: bytes=...` (HTTP 206 Partial Content).
  * Pipeline automático de legendas pt-BR via OpenSubtitles v3 / Cinemeta já integrado ao ecossistema do CineLocal.
  * HUD de buffer, seeds e velocidade de download diretamente na barra do player.

### C. CineLocal Desktop: Aplicativo Instalável Autônomo (Issue #17)
* **Objetivo:** Empacotar todo o ecossistema (servidor Python embutido, FFmpeg, interface e utilitários) em um instalador oficial `.exe` para Windows sem dependência de scripts `.bat` ou instalação prévia de Python pelo usuário final.
* **Componentes:**
  * **Instalador Oficial (`CineLocal-Setup.exe`):** Criado via Inno Setup com atalhos na Área de Trabalho e Menu Iniciar.
  * **Painel Unificado de Gerenciamento:** Botões de scan de catálogo, busca TMDb, otimização de áudio e chave de servidor para Smart TV centralizados dentro da própria interface web.
