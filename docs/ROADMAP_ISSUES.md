# 📋 Backlog de Funcionalidades & Issues do CineLocal

Este documento formaliza as issues, refinamentos arquiteturais, fluxogramas de dados e planos de implementação para consolidar o **CineLocal** como uma plataforma completa de streaming e gerenciamento de mídia local.

---

## 📌 Issue #15: Web Media Manager & Local-First Cloud App (Subir Site + Filmes Locais via File System API)
> 🔗 **GitHub Issue:** [#15](https://github.com/rniguel/cinelocal/issues/15)

### 🎯 1. Visão Geral & Nova Arquitetura Web (Cloud-Deployable + Local-First)
Transformar o **CineLocal** em uma aplicação web moderna que pode ser **hospedada publicamente na internet** (Vercel, Netlify, Cloudflare Pages ou GitHub Pages), permitindo que qualquer pessoa acesse uma URL simples (ex: `https://cinelocal.app`) e conecte sua biblioteca de filmes **diretamente do seu próprio computador**, sem fazer upload de nenhum vídeo para a nuvem e sem precisar instalar Python ou rodar servidores locais!

---

### 💡 2. O Segredo Tecnológico: File System Access API + Blob Streaming

```text
[Usuário Acessa o Site na Nuvem: https://cinelocal.vercel.app]
                            │
                            ▼
      [Clica em: "Conectar Minha Pasta de Filmes"]
                            │
                            ▼
              [Navegador Pede Permissão Nativa]
          ("Permitir que o site acesse D:\Filmes?")
                            │
                            ▼
   [File System Access API (showDirectoryPicker) + IndexedDB]
                            │
       ┌────────────────────┴────────────────────┐
       ▼                                         ▼
[Catalogação & Metadados]                [Reprodução de Vídeo]
- Varre arquivos no disco local          - Gera Blob URLs locais:
- Limpa tags de release via Regex          `URL.createObjectURL(fileHandle)`
- Consulta TMDb API (Capas + Sinopses)   - Toca a 0ms no player nativo
- Salva cache de metadados no IndexedDB  - ZERO bytes enviados para a nuvem!
       │                                         │
       └────────────────────┬────────────────────┘
                            ▼
      [Web Media Manager & Organizador no Disco Local]
      - Permissão 'readwrite'
      - Cria pastas: dirHandle.getDirectoryHandle("Nome (Ano)", {create: true})
      - Salva capa oficial: baixa do TMDb e grava `poster.jpg` local
      - Move/Organiza arquivos de vídeo no disco do usuário
```

---

### 🌟 3. Principais Pilares da Funcionalidade

#### A. Zero Instalação & Zero Custo de Hospedagem
* **Sem Python / Sem Terminal:** Qualquer usuário pode apenas abrir o link no navegador (Google Chrome, Microsoft Edge, Brave, Opera).
* **Custos Zero de Servidor:** Como os arquivos de vídeo (5GB a 20GB) nunca passam pelo servidor da nuvem, a hospedagem consome apenas tráfego de arquivos estáticos (HTML/CSS/JS), ficando 100% gratuita na Vercel ou Netlify.

#### B. Persistência de Pastas com IndexedDB
* Quando o usuário conecta a pasta `D:\Filmes`, o navegador armazena o `FileSystemDirectoryHandle` serializado no **IndexedDB**.
* Ao fechar o navegador e voltar ao site no dia seguinte, a biblioteca inteira já carrega automaticamente sem necessidade de selecionar a pasta novamente.

#### C. Web Media Manager & Organizador de Pastas no Próprio Disco
Com a permissão `readwrite` concedida pelo usuário:
1. **Adicionar Novo Filme:**
   * Usuário pesquisa pelo título no TMDb (cards com posters e sinopse em pt-BR).
   * Clica em "Selecionar Arquivo de Vídeo" (`showOpenFilePicker()`).
   * O site cria a pasta oficial `Nome do Filme (Ano)/` no disco dele, baixa o pôster em alta resolução como `poster.jpg` e move/copia o arquivo.
2. **Organizador de Pastas em Lote (Batch Importer):**
   * O site analisa uma pasta cheia de downloads desorganizados, identifica cada título limpando os nomes com Regex (`1080p`, `WEB-DL`, `x264`, `DUAL`, `1XBET`), busca as capas no TMDb e oferece um botão: **"Organizar Pastas no meu Disco"**.

#### D. Modo Dual (Híbrido)
* **Modo Web Puro (Cloud):** Acesso via link web público, tocando arquivos locais via Blob URLs e File System Access API.
* **Modo Servidor Local (Desktop):** Mantém suporte ao backend Python (`servidor.py`) para quem deseja usar o controle remoto na TV (`/remote`), VLC integrado e transcodificação FFmpeg.

---

### 💡 2. O Desafio do Navegador e a Solução Nativa Local

```text
[Arquivos Locais: Downloads / Torrents / HD Externo]
                      │
                      │ (Usuário informa caminho no Web App)
                      ▼
[CineLocal Web App (Frontend)] ──POST /api/media/import──► [servidor.py (Backend Local)]
                                                                  │
                                                ┌─────────────────┴─────────────────┐
                                                ▼                                   ▼
                                      [Consulta API TMDb]                 [Sistema de Arquivos Local]
                                  (Metadados + poster.jpg)            (Mover/Copiar sem upload HTTP)
                                                │                                   │
                                                └─────────────────┬─────────────────┘
                                                                  ▼
                                              [media/filmes/Nome (Ano)/...]
                                                                  │
                                                                  ▼
                                              [atualizar_catalogo.py em memória]
                                                                  │
                                                                  ▼
                                        [Filme visível e pronto no Web App!]
```

* **Restrição de Sandbox Web:** Navegadores bloqueiam o acesso a caminhos absolutos do sistema operacional (`C:\Downloads\...`) a partir de `<input type="file">`. Um upload convencional via formulário web transferiria arquivos de 5 a 20 GB pela rede local, tornando o processo lento e consumindo CPU desnecessária.
* **Solução do CineLocal:** Como o CineLocal executa o servidor local (`app/servidor.py`) com privilégios do usuário no computador, a interface web envia apenas o **caminho absoluto (path) do arquivo ou pasta**. O backend em Python realiza a operação de `shutil.move()` ou `shutil.copy2()`, transferindo arquivos em milissegundos (na mesma partição) ou com taxa máxima de barramento do disco, sem tráfego HTTP desnecessário.

---

### 🎨 3. Especificação da Interface Web (UI/UX)

#### A. Botão de Acesso Rápido no Header
* Novo botão flutuante/estilizado no cabeçalho: `+ Adicionar / Organizar`.
* Ao clicar, abre o modal responsivo `MediaManagerModal` com abas dedicadas:
  * **Aba 1: Adicionar Novo Título (Fluxo Guiado)**
  * **Aba 2: Organizar Pasta de Downloads (Batch Importer)**
  * **Aba 3: Gerenciar Pastas & Bibliotecas**

#### B. Aba 1: Adicionar Novo Título (Fluxo Guiado em 3 Passos)
1. **Passo 1: Identificação no TMDb**
   * Input de texto com debounce de 350ms consultando `/api/tmdb/search`.
   * Cards de resultado com pôster, título em português, ano, sinopse curta e nota.
   * Seleção em 1 clique do título correspondente.
2. **Passo 2: Vinculação do Arquivo de Vídeo**
   * Input para colar o caminho do arquivo local (ex: `D:\Downloads\filme_baixado.mkv`).
   * Sugestor rápido com botão "Arquivos Recentes em Downloads" (o servidor lista os últimos `.mkv`/`.mp4` modificados na pasta padrão de Downloads do usuário).
   * Opções de transferência com explicações visuais:
     * 🟢 **Mover (Recomendado):** Move o arquivo para a pasta definitiva do CineLocal. Praticamente instantâneo e não duplica espaço no disco.
     * 🔵 **Copiar:** Mantém o original na pasta de origem e cria uma cópia estruturada na pasta de mídia.
3. **Passo 3: Confirmação & Execução**
   * Exibição do resumo: caminho de destino previsto (`media/filmes/Titulo (Ano)/Titulo (Ano) [1080p].ext`).
   * Botão "Processar e Adicionar à Biblioteca".
   * Feedback visual com barra de progresso / loader.
   * Conclusão com modal de sucesso e botão **"Assistir Agora"** (iniciando o player imediatamente).

#### C. Aba 2: Organizar Pasta de Downloads (Batch Importer)
* Campo para apontar uma pasta (ex: `D:\Torrents` ou `C:\Users\...\Downloads`).
* O backend lista todos os vídeos e executa o algoritmo de limpeza de nomes (`clean_movie_title`):
  * Remove termos de release: `1080p`, `720p`, `x264`, `x265`, `WEB-DL`, `DUAL`, `1XBET`, `BLUDV`, etc.
  * Extrai o ano provável e consulta sugestões do TMDb.
* Exibição de tabela com preview:
  * [x] Nome Original do Arquivo ➔ [Sugestão TMDb com Capa] ➔ Botão de trocar match.
* Botão de ação: **"Organizar e Importar Selecionados"**.

---

### 🔌 4. Endpoints de Backend a Implementar (`app/servidor.py`)

| Rota | Método | Parâmetros / Body | Descrição |
|---|---|---|---|
| `/api/tmdb/search` | `GET` | `query`, `type` (movie/tv), `year` | Busca títulos no TMDb com metadados em pt-BR e URL de pôster. |
| `/api/media/browse_recent` | `GET` | `folder` (opcional) | Lista arquivos de vídeo recentes na pasta de Downloads ou informada. |
| `/api/media/import` | `POST` | `{ tmdbId, title, year, sourcePath, action, mediaType, ... }` | Cria pastas, baixa poster.jpg, move/copia o arquivo, atualiza metadados e catálogo. |
| `/api/media/scan_batch` | `POST` | `{ folderPath }` | Escaneia pasta de vídeos, limpa títulos e sugere matches no TMDb. |
| `/api/media/execute_batch` | `POST` | `{ items: [...] }` | Executa importação em lote com retorno de progresso. |

---

## 📌 Issue #16: Engine de Streaming de Torrent & Magnet Links no Player (Estilo Stremio)
> 🔗 **GitHub Issue:** [#16](https://github.com/rniguel/cinelocal/issues/16)

### 🎯 1. Visão Geral e Proposta de Valor
Permitir que o usuário assista a filmes e episódios através de **Magnet Links** ou arquivos `.torrent` diretamente no CineLocal, iniciando a reprodução em poucos segundos **sem necessidade de download prévio completo**.

---

### 🔍 2. Análise Técnica e Princípio de Funcionamento

```text
[Magnet Link / Arquivo .torrent]
               │
               ▼
+───────────────────────────────────────────────────────────────+
|               CineLocal Torrent Stream Engine                 |
|                                                               |
| 1. Análise de Metadados:                                      |
|    - Conecta aos trackers / DHT e obtém lista de arquivos     |
|    - Seleciona automaticamente o arquivo de vídeo principal   |
|                                                               |
| 2. Download Sequencial com Janela Deslizante (Sliding Window):|
|    - Prioridade Máxima: Primeiras peças (cabeçalho de vídeo)  |
|    - Prioridade Alta: Últimas peças (índice de busca / moov)  |
|    - Janela Ativa: Peças próximas à posição atual de play     |
|                                                               |
| 3. Buffer Inicial & Servidor HTTP 206:                        |
|    - Acumula buffer inicial (15 MB a 40 MB)                   |
|    - Abre endpoint HTTP com suporte a Range Requests:         |
|      http://localhost:8000/api/torrent/stream?hash=...        |
+───────────────────────────────┬───────────────────────────────+
                                │
                                ▼
+───────────────────────────────────────────────────────────────+
|                      Player Web CineLocal                     |
|                                                               |
| - Reprodução instantânea via <video> com Range Requests       |
| - Download automático de legendas pt-BR (OpenSubtitles v3)    |
| - HUD discreto com velocidade (MB/s), seeds e buffer          |
| - Opção: "Salvar na Biblioteca Permanente ao Concluir"        |
+───────────────────────────────────────────────────────────────+
```

---

### ⚙️ 3. Comparativo de Motores de Execução (Engine)

#### Opção 1: Micro-serviço WebTorrent / Torrent-Stream (Padrão Stremio)
* **Como opera:** O Stremio utiliza o `torrent-stream` (módulo Node.js ultra-otimizado para streaming sequencial).
* **Vantagens:**
  * Estabilidade e maturidade comprovadas com milhões de usuários ativos no ecossistema Stremio.
  * Excelente suporte a reprodução durante o download com seek rápido.
  * Suporte a WebRTC e DHT descentralizada.
* **Implementação no CineLocal:**
  * Pode ser executado como um processo auxiliar leve empacotado ou instalado sob demanda.
  * O `servidor.py` gerencia o ciclo de vida da engine (inicia apenas quando uma reprodução torrent for solicitada e encerra após inatividade).

#### Opção 2: Engine Python Nativa (`libtorrent`)
* **Como opera:** Utiliza bindings de `libtorrent` (o mesmo motor utilizado por qBittorrent e Deluge), com a flag de download sequencial ativada (`set_sequential_download(True)`).
* **Vantagens:**
  * Mantém o projeto 100% contido em Python, sem dependência de ambientes externos.
  * Performance em C++ nativo com baixíssimo consumo de memória RAM.

---

### 🎬 4. Experiência de Reprodução & Superpoderes do CineLocal

1. **Modal "Assistir via Torrent":**
   * Campo para colar o Magnet Link ou fazer drag-and-drop de um arquivo `.torrent`.
   * Busca automática do título no Cinemeta/TMDb a partir do nome contido no torrent para exibir o pôster e a sinopse.
2. **Buffer Inicial com Feedback Visual:**
   * Barra de carregamento inteligente mostrando:
     * Número de sementes ativas (ex: `🟢 54 seeds`).
     * Taxa de download em tempo real (ex: `🚀 6.8 MB/s`).
     * Percentual do buffer inicial necessário para dar o play sem travamentos (ex: `100% carregado - Iniciando...`).
3. **Legendas em Português Automáticas:**
   * O CineLocal já possui o endpoint `/api/buscar_legendas` conectado com a API Cinemeta/OpenSubtitles v3. Ao reconhecer o hash ou nome do filme, ele baixa a legenda `.srt` em português de forma 100% automatizada.
4. **Áudio e Controles Completos:**
   * Seleção de áudio, atalhos de teclado, controle remoto móvel (`/remote`) e Super Booster de som até 300% continuam funcionando normalmente.
5. **Opção de Salvar na Coleção:**
   * O arquivo que está sendo baixado em cache temporário pode ser transferido com um clique para a pasta `media/filmes/Nome (Ano)` ao término da sessão, transformando o streaming em uma adição permanente ao catálogo.

---

---

## 📌 Issue #17: CineLocal Desktop: Aplicativo Instalável Autônomo (.exe) com Painel Unificado
> 🔗 **GitHub Issue:** [#17](https://github.com/rniguel/cinelocal/issues/17)

### 🎯 1. Visão Geral e Proposta de Valor
Transformar o CineLocal em um **aplicativo desktop instalável autônomo** (com instalador `.exe` oficial para Windows), unificando todas as ferramentas, scripts e utilitários que hoje rodam em arquivos `.bat` separados diretamente dentro da interface gráfica da aplicação.

---

### 💡 2. O Problema Atual vs. A Solução do Instalável
* **Hoje:** O usuário precisa ter o Python instalado no computador, abrir pastas e dar duplo clique em scripts `.bat` separados (`Atualizar Catalogo.bat`, `Buscar Metadados (TMDb).bat`, `Iniciar Servidor.bat`, `Otimizar Audio Web.bat`). Janelas pretas de terminal aparecem na tela, o que pode assustar usuários leigos.
* **Com o Instalador Oficial (`CineLocal-Setup.exe`):**
  1. O usuário baixa um instalador tradicional do Windows (`.exe`).
  2. Instala com o assistente padrão ("Avançar ➔ Avançar ➔ Concluir").
  3. Ganha atalhos automáticos na Área de Trabalho e no Menu Iniciar com o ícone cinematográfico do CineLocal.
  4. O Python e todas as dependências vêm **embutidos** no app (não precisa instalar nada por fora).
  5. Ao abrir, o CineLocal inicia em uma janela dedicada sem terminal preto visível.

---

### 🎛️ 3. Painel de Controle Integrado na Interface (Fim dos Scripts `.bat`)
Todas as rotinas que antes eram scripts externos passam a ter botões e painéis visuais dentro do menu **Configurações / Painel de Mídia** do CineLocal:
* **🔄 Atualizar Catálogo em 1 Clique:** Botão na navbar que escaneia o disco, detecta novas mídias e recarrega os carrosséis instantaneamente.
* **🧠 Enriquecedor de Metadados TMDb:** Modal visual mostrando barra de progresso de busca de sinopses e posters.
* **🔊 Otimizador de Áudio Web Integrado:** Fila visual de processamento de áudio para AAC estéreo via FFmpeg sem abrir janelas CMD.
* **📡 Servidor para Smart TV e Celular (Toggle Switch):** Chave ON/OFF na interface com exibição do IP local e botão de abrir o QR Code do controle remoto.
* **📁 Seletor de Pastas de Mídia:** Diálogo nativo do Windows para escolher onde os filmes e séries estão guardados.

---

## 🗓️ 5. Cronograma e Etapas de Entrega

```mermaid
flowchart TD
    subgraph Fase 1: Web Media Manager
        F1A["Endpoint TMDb Search & Recent Files"] --> F1B["Modal Adicionar Filme no Frontend"]
        F1B --> F1C["Endpoint de Importação (Move/Copy + Poster)"]
        F1C --> F1D["Recompilação Automática do Catálogo"]
    end

    subgraph Fase 2: Batch Importer
        F2A["Scanner de Pastas de Downloads"] --> F2B["Regex Cleaner de Títulos & TMDb Matcher"]
        F2B --> F2C["Interface de Revisão e Organização em Lote"]
    end

    subgraph Fase 3: Torrent Streaming Engine
        F3A["Integração da Engine de Torrent Sequencial"] --> F3B["Endpoint HTTP 206 para Stream de Peças"]
        F3B --> F3C["Modal Magnet Link & HUD de Buffer no Player"]
        F3C --> F3D["Download Automático de Legendas pt-BR no Stream"]
    end

    Fase 1 --> Fase 2 --> Fase 3
```

---

## 📋 Checklist de Validação das Regras do CineLocal
- [x] **Preservação de Mídia:** Nenhuma rotina de importação ou organização apagará arquivos de vídeo existentes sem confirmação explícita.
- [x] **Sincronização de UI:** Qualquer modificação na interface do usuário será refletida no mestre `app/generate_netflix_ui.py` e compilada em `app/index.html`.
- [x] **Atualização de Catálogo:** Disparo automático de `atualizar_catalogo.py` em memória após qualquer movimentação de arquivos.
- [x] **Codificação:** Todos os novos scripts e manipuladores utilizam rigorosamente `utf-8` e sanitização de paths para Windows.
