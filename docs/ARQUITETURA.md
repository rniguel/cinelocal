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
   [index.html] (Frontend SPA / Web Audio 200% / VLC Triggers)
        ▲
        │
   [servidor.py] ────► [VLC Media Player (vlc.exe)]
```

---

## 🖥️ 1. Frontend (`app/index.html` & `app/generate_netflix_ui.py`)

* **Tecnologia:** HTML5 Semântico, CSS Moderno com Variáveis Customizadas, e JavaScript Vanilla puro (sem dependências de frameworks pesados para garantir carregamento instantâneo de milissegundos).
* **Estrutura de Componentes:**
  * **Header:** Barra de navegação com marca, chips de visualização (*Home*, *Filmes*, *Séries*), atalhos para *Surpreenda-me* (🎲 Roleta), *TV / Celular* (📱 QR Code) e campo de busca global em tempo real.
  * **Hero Banner:** Destaque visual randômico ou curado com imagem de alta resolução, metadados completos e botões de reprodução rápida.
  * **Carrosséis Horizontais com Suporte a Touch e Botões:**
    * *⏱️ Continuar Assistindo* (Itens em andamento com barra de progresso individual e tempo restante)
    * *🔥 Adicionados Recentemente* (Ordenados pelo timestamp de modificação real `addedAt`)
    * *📺 Séries & Temporadas*
    * *⚡ Universo Marvel (Ordem Cronológica do MCU)* com Card de Destaque Interativo
    * *🏆 Grandes Franquias & Sagas Épicas*
    * *🎬 Catálogo Geral de Longas-Metragens*
  * **Filtros do Catálogo de Filmes:**
    * Gênero dinâmico (Ação, Drama, Ficção, etc.)
    * Ano / Décadas (2020+, 2010s, 2000s, Clássicos)
    * Status de visualização (*Não Assistidos*)
  * **Player Cinematográfico Integrado:**
    * Implementado sobre a tag `<video>` do HTML5.
    * **Controles Inteligentes:** Ocultação automática após inatividade durante reprodução e exibição permanente no pause.
    * **Clique na Tela:** Pausa/reproduz clicando em qualquer ponto da tela, com pulso visual centralizado estilo YouTube.
    * **Picture-in-Picture (PiP):** Janela flutuante nativa do navegador (`document.pictureInPictureElement`).
    * **Velocidade Dinâmica:** Taxas de 0.75x a 2.0x configuráveis por botão e atalhos de teclado (`[` e `]`).
    * **Contagem de Próximo Episódio:** Toast flutuante nos últimos 20 segundos de um episódio para avançar automaticamente.
    * **Persistência de Progresso:** Salva o ponto exato da reprodução e estado de assistido no `localStorage`.
    * **Nó de Áudio Web:** `AudioContext` + `GainNode` permitindo amplificação de volume de até 300%.
  * **Navegação Smart TV & D-Pad:**
    * Motor de foco espacial para setas do controle remoto (`↑`, `↓`, `←`, `→`) e `Enter / OK`.
    * Destaque com brilho luminoso (`:focus-visible` e `.tv-focused`).
  * **Modais Reativos:**
    * `#movieDetailsModal`: Ficha completa do filme com sinopse, elenco, botão de continuar assistindo, marcar como assistido, links TMDb/IMDb e opções de reprodução.
    * `#seriesModal`: Seletor de temporadas e episódios com marcação de assistido.
    * `#surpriseModal`: Roleta aleatória que sorteia produções bem avaliadas do acervo.
    * `#qrModal`: Exibe QR Code e endereço IP para emparelhamento instantâneo com celulares e Smart TVs.
    * `#mcuTrackerModal`: Linha do tempo de 66 produções da Marvel, monitoramento de coleção e filtros dinâmicos.

---

## ⚙️ 2. Backend & Servidor Local (`app/servidor.py`)

* **Tecnologia:** Python nativo utilizando `http.server.ThreadingHTTPServer` para atender múltiplas conexões simultâneas de computadores, Smart TVs e celulares.
* **Recursos Especiais do Servidor:**
  * **HTTP Range Requests (Bytes 206 Partial Content):** Permite navegação rápida na barra de tempo do vídeo (*seek*) sem necessidade de baixar o arquivo inteiro.
  * **Endpoint `/api/capabilities`:** Informa se o VLC e FFmpeg estão disponíveis, além de expor o IP da rede local (`localIp`) e URL completa (`localUrl`) para o modal de conexão QR Code.
  * **Endpoint `/api/open_vlc`:** Recebe requisições da interface web e executa o VLC Media Player nativo no Windows de forma assíncrona e em background, priorizando caminhos padrão e portáteis.
  * **Detecção Automática de IP Local:** Descobre e imprime no terminal o IP da máquina na rede Wi-Fi/Ethernet (ex: `http://192.168.1.15:8000`), gerando comodidade para quem acessa via Smart TV ou celular.

---

## ⚡ 3. Compilador de Mídia (`app/atualizar_catalogo.py`)

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

## 🌐 4. Enriquecedor de Metadados TMDb (`app/buscar_metadados_tmdb.py`)

* **Operação Desacoplada e Opcional:**
  * Não interfere no funcionamento offline padrão do CineLocal.
  * Realiza consultas via API v3 do TMDb em português brasileiro (pt-BR).
  * Faz download de pôsteres oficiais (`poster.jpg`) somente nas pastas que não tiverem imagem.
  * **Preservação de Mídia:** Nunca altera, move ou renomeia os arquivos de vídeo.
