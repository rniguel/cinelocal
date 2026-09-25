# 🤖 Diretrizes e Regras do CineLocal para Gemini / IA

Este documento define os padrões arquiteturais, regras operacionais e boas práticas para qualquer assistente de inteligência artificial (Gemini, Antigravity, etc.) atuando na manutenção ou expansão do ecossistema **CineLocal**.

---

## 📌 1. Regras Fundamentais e Invioláveis

1. **PRESERVAÇÃO ABSOLUTA DE MÍDIA:**
   * **NUNCA** apague arquivos de vídeo (`.mkv`, `.mp4`, `.avi`) sem comando explícito e direto do usuário.
   * Ao limpar pastas, exclua apenas arquivos de propaganda e lixo (`.url`, `.txt`, arquivos `1XBET`, `BLUDV.mp4`, etc.).

2. **SINCRONIZAÇÃO DA INTERFACE (REGRA DE OURO):**
   * O arquivo `app/generate_netflix_ui.py` é o gerador oficial de `app/index.html`.
   * **Sempre que modificar a interface (HTML, CSS ou JavaScript do frontend)**, aplique a alteração no script `app/generate_netflix_ui.py` e execute `python app/generate_netflix_ui.py` para regenerar `app/index.html`.
   * Isso garante que `generate_netflix_ui.py` e `index.html` permaneçam 100% sincronizados.

3. **ATUALIZAÇÃO DE CATÁLOGO APÓS ALTERAÇÕES:**
   * Sempre que arquivos de mídia forem adicionados, renomeados, movidos ou tiverem legendas baixadas, execute `python app/atualizar_catalogo.py` para atualizar o `app/catalogo.js`.

4. **CODIFICAÇÃO E COMPATIBILIDADE WINDOWS:**
   * Todos os scripts Python devem abrir e salvar arquivos com `encoding='utf-8'` (ou `utf-8-sig` para legendas).
   * Utilize `os.path.normpath` ou trate barras invertidas `\\` para barras normais `/` nos caminhos servidos ao navegador.

---

## 🗂️ 2. Padrões de Mídia e Nomenclatura

* **Filmes Avulsos:**
  `media/filmes/Nome do Filme (Ano)/Nome do Filme (Ano) [Resolução].ext`
  Exemplo: `media/filmes/Interestelar (2014)/Interestelar (2014) [1080p].mkv`

* **Franquias com Ordem Cronológica / Sequencial:**
  `media/filmes/NomeFranquia/01 - Titulo (Ano)/Titulo (Ano) [Resolução].ext`
  Exemplo Marvel: `media/filmes/Marvel/06 - Deadpool 2 (2018)/Deadpool 2 (2018) [720p].mp4`

* **Séries:**
  `media/series/Nome da Serie/Season 01/Nome da Serie - S01E01.ext`
  Exemplo: `media/series/Loki/Season 01/Loki - S01E01.mkv`

* **Posters:**
  Salvar como `poster.jpg` na raiz da pasta do filme ou série (proporção 2:3, preferencialmente oficial do TMDb em português).

* **Legendas:**
  Salvar no formato `.srt` com o mesmo nome base do vídeo ou com sufixos identificadores (`.forced.srt`, `.pt.srt`).

---

## ⚡ 3. Universo Cinematográfico Marvel (MCU)

* A coleção da Marvel segue a **Ordem Cronológica Canônica** definida pelo usuário (com números de sequência `#01` a `#16` na coleção local).
* As séries **Loki** (#09) e **WandaVision** (#10) possuem mapeamento especial em `SERIES_FRANCHISE` dentro de `app/atualizar_catalogo.py` para serem indexadas no carrossel da Marvel.
* O rastreador geral do MCU (`window.MCU_CANONICAL_TIMELINE` em `generate_netflix_ui.py`) monitora todas as 66 produções oficiais da Marvel Studios até 2026. Ao adicionar um novo filme ou série da Marvel, garanta que suas palavras-chave em `keywords` permitam a correspondência automática no rastreador.

---

## 🧠 4. Banco de Metadados (`app/metadata_db.py`)

* Novos títulos devem ser inseridos em `MOVIES_METADATA` ou `SERIES_METADATA` em `app/metadata_db.py` com:
  * `overview`: Sinopse rica e autêntica em português (pt-BR).
  * `cast`: Lista com 4 a 6 atores principais.
  * `director` / `creator`: Diretor ou criador oficial.
  * `genres`: Lista de gêneros.
  * `rating`: Nota média (ex: TMDb / IMDb).
  * `tmdbUrl`: Link oficial do filme/série no TMDb.
  * `imdbUrl`: Link oficial no IMDb.

---

## 🔊 5. Tratamento de Áudio e Codecs

* O player nativo dos navegadores (Google Chrome / Edge) suporta codecs `aac`, `mp3`, `opus`.
* Para formatos avançados de cinema (**DTS-HD, TrueHD, AC3 7.1**), o CineLocal oferece o botão **Abrir no VLC**, que chama o binário local do VLC via endpoint `http://localhost:8000/launch_vlc?path=...`.
* Caso o usuário queira reprodução exclusiva no navegador para arquivos com áudio mudo, utilize `otimizar_audio_web.py`, que adiciona uma faixa estéreo AAC sem recodificar o vídeo (`-c:v copy`).
