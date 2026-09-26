# 🛠️ Scripts Utilitários do CineLocal

Este documento detalha o propósito, parâmetros e funcionamento de cada script utilitário localizado na pasta `app/` e seus atalhos na raiz.

---

## 1. `atualizar_catalogo.py` / `Atualizar Catalogo.bat`

* **Objetivo:** Escanear as pastas `media/filmes` e `media/series`, extrair metadados, analisar trilhas de áudio/legendas via FFmpeg e compilar a base de dados `app/catalogo.js`.
* **Como Executar:**
  * Pelo terminal: `python app/atualizar_catalogo.py`
  * Pelo Windows Explorer: Dê dois cliques em `Atualizar Catalogo.bat` na raiz.
* **Mecanismos Internos:**
  * **Sistema de Cache (`app/.audio_cache.json`):** Armazena o hash/timestamp (`mtime`) de cada arquivo de vídeo. O scanner só analisa arquivos com FFmpeg quando eles são novos ou foram modificados, tornando a execução praticamente instantânea para coleções grandes.
  * **Higienização de Legendas:** Lê os arquivos `.srt`, converte para UTF-8 sem BOM, remove tags HTML inválidas (`<font color="...">`, `{y:i}`, etc.) e injeta o dicionário no `window.LEGENDAS_DB`.
  * **Associação de Franquias & Séries:** Mapeia séries da Marvel (como Loki e WandaVision) e franquias numeradas com suas posições cronológicas.

---

## 2. `generate_netflix_ui.py`

* **Objetivo:** Gerador mestre da interface `app/index.html`.
* **Como Executar:** `python app/generate_netflix_ui.py`
* **Por que utilizar?**
  * Mantém o código do frontend centralizado, documentado e versionado.
  * Permite injeção de novos estilos, templates, componentes e lógicas JavaScript sem perder compatibilidade ou corromper o arquivo HTML final.

---

## 3. `servidor.py` / `Iniciar Servidor (TV e Celular).bat`

* **Objetivo:** Servidor HTTP local multithreaded que serve o CineLocal para o computador, Smart TV, celular e tablet.
* **Como Executar:**
  * Pelo terminal: `python app/servidor.py`
  * Pelo Windows Explorer: Dê dois cliques em `Iniciar Servidor (TV e Celular).bat` na raiz.
* **Recursos Avançados:**
  * **Descoberta de IP de Rede:** Identifica a interface de rede ativa e exibe a URL local pronta para uso (ex: `http://192.168.1.15:8000`).
  * **HTTP Range Requests (RFC 7233):** Atende requisições de bytes parciais (`206 Partial Content`), essenciais para que o player do navegador consiga avançar ou retroceder (*seek*) vídeos pesados sem travamentos.
  * **Hub de Controle Remoto para Smartphones (`/remote`):** Hub de eventos em tempo real (`RemoteControllerHub`) utilizando Server-Sent Events (SSE). Permite que o smartphone controle a Smart TV ou PC com latência mínima (< 20ms) e sem necessidade de teclado/mouse.
  * **Sincronização de Progresso e Favoritos (`/api/progress` e `/api/favorite/toggle`):** Armazena o estado do usuário de forma segura em `app/data/user_state.json`. Quando você pausa um filme no computador, o tempo assistido e os favoritos são atualizados automaticamente na Smart TV.
  * **Inspeção de Trilhas de Áudio (`/api/audio_info`):** Executa o `ffprobe` para ler as faixas de áudio embutidas no arquivo de vídeo e expor para seleção no player web.
  * **Integração com VLC (`/api/open_vlc`):** Endpoint que aceita parâmetros de caminho e abre o VLC Media Player de 64 bits em segundo plano de forma instantânea.

---

## 4. `otimizar_audio_web.py` / `otimizar_audio_web.bat`

* **Objetivo:** Converter faixas de áudio que não reproduzem som no Google Chrome (como DTS, DTS-HD ou TrueHD) para o codec AAC estéreo compatível com a web.
* **Como Executar:**
  * Dê dois cliques em `app/otimizar_audio_web.bat`.
* **Diferencial de Performance:**
  * Utiliza `-c:v copy`, preservando 100% da imagem original sem reencodar o vídeo. O processo leva apenas alguns segundos mesmo em vídeos 1080p ou 4K de muitos gigabytes.

---

## 5. `metadata_db.py`

* **Objetivo:** Dicionário de enriquecimento cultural e metadados cinematográficos para filmes e séries.
* **Estrutura:**
  * `MOVIES_METADATA`: Sinopses originais em português, elencos, diretores, gêneros e notas para filmes avulsos e franquias.
  * `SERIES_METADATA`: Dados completos de séries de TV (Loki, WandaVision, Arcane, Chernobyl, The Bear, etc.).
  * **Fallback Inteligente:** Caso um filme não tenha entrada cadastrada, a função `get_movie_info` gera uma descrição contextual com links de busca no TMDb e IMDb.
