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
  * **Header:** Barra de navegação com marca, chips de visualização (*Home*, *Filmes*, *Séries*) e campo de busca global em tempo real com limpeza rápida.
  * **Hero Banner:** Destaque visual randômico ou curado com imagem de alta resolução, metadados completos e botão de play imediato.
  * **Carrosséis Horizontais com Suporte a Touch e Botões:**
    * *Adicionados Recentemente*
    * *Séries & Temporadas*
    * *Universo Marvel (Ordem Cronológica do MCU)* com Card de Destaque Interativo
    * *Grandes Franquias & Sagas Épicas*
    * *Catálogo Geral de Longas-Metragens*
  * **Player Cinematográfico Integrado:**
    * Implementado sobre a tag `<video>` do HTML5.
    * Suporte a faixas de legendas `.vtt` / `.srt` convertidas on-the-fly.
    * Menu lateral de legendas com busca de diálogos e salto de tempo.
    * Nó de áudio via **Web Audio API** (`AudioContext` + `GainNode`) permitindo **Boost de Volume até 200%**.
  * **Modais Reativos:**
    * `#movieDetailsModal`: Ficha completa do filme com sinopse, elenco, gênero, links TMDb/IMDb e opções de reprodução.
    * `#seriesModal`: Seletor de temporadas e episódios com cards informativos individuais.
    * `#mcuTrackerModal`: Linha do tempo de 66 produções da Marvel, monitoramento de coleção e filtros dinâmicos.

---

## ⚙️ 2. Backend & Servidor Local (`app/servidor.py`)

* **Tecnologia:** Python nativo utilizando `http.server.ThreadingHTTPServer` para atender múltiplas conexões simultâneas de computadores, Smart TVs e celulares.
* **Recursos Especiais do Servidor:**
  * **HTTP Range Requests (Bytes 206 Partial Content):** Permite navegação rápida na barra de tempo do vídeo (*seek*) sem necessidade de baixar o arquivo inteiro.
  * **Detecção Automática de IP Local:** Descobre e imprime no terminal o IP da máquina na rede Wi-Fi/Ethernet (ex: `http://192.168.1.15:8000`), gerando comodidade para quem acessa via Smart TV ou celular.
  * **Endpoint `/launch_vlc`:** Recebe requisições da interface web e executa o VLC Media Player nativo no Windows de forma assíncrona e em background, priorizando `C:\Program Files\VideoLAN\VLC\vlc.exe`.

---

## ⚡ 3. Compilador de Mídia (`app/atualizar_catalogo.py`)

* **Escaneamento Automatizado:**
  * Percorre recursivamente `media/filmes` e `media/series`.
  * Detecta resoluções no nome do arquivo (`2160p`, `4K`, `1080p`, `720p`).
  * Associa pastas de franquia e numerações de sequência.
* **Cache Inteligente de Áudio (`.audio_cache.json`):**
  * Salva o timestamp (`mtime`) de cada arquivo de vídeo já analisado.
  * Quando um filme ou série não foi alterado, o probe é recuperado instantaneamente da memória sem gastar CPU com o FFmpeg.
  * Se um arquivo for substituído ou adicionado, o sistema detecta a alteração e atualiza apenas a mídia modificada.
* **Higienização de Legendas:**
  * Lê arquivos `.srt` em múltiplas codificações (`utf-8`, `utf-8-sig`, `cp1252`, `latin-1`).
  * Remove tags indesejadas de fontes (`<font color="...">`, `{y:i}`, etc.), garantindo sincronismo e exibição límpida.
* **Geração de Saída:**
  * Compila `catalogo.js` contendo `window.CATALOGO`, `window.CATALOGO_FILMES`, `window.CATALOGO_SERIES` e `window.LEGENDAS_DB`.
