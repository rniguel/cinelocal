# 🎬 CineLocal - Home Theater & Streaming Doméstico

Bem-vindo ao **CineLocal**, sua central de streaming multimídia de alta performance para reproduzir sua coleção local de filmes e séries com uma experiência visual inspirada na Netflix.

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

### 2. ⚡ Universo Cinematográfico Marvel (MCU) & Rastreador Canônico
* **Ordem Cronológica do MCU:** Carrossel especial com os filmes e séries numerados em sequência narrativa canônica (#01 a #16).
* **Guia & Rastreador da Linha do Tempo (66 Produções):** 
  * Modal interativo com todos os 66 títulos oficiais da Marvel Studios (da década de 1940 até os lançamentos de 2026).
  * Mostra em tempo real quais títulos já estão **Disponíveis na sua Coleção CineLocal** (`✓ NA COLEÇÃO`) e quais faltam baixar.
  * Estatísticas ao vivo: total de produções, quantidade disponível, faltantes e barra de progresso percentual.
  * Busca e filtros por status (*Na Coleção*, *Faltando Baixar*, *Filmes*, *Séries*).
  * Botões de reprodução direta integrados: clique em *Assistir ▶* em qualquer título da Marvel no rastreador para dar play imediato!

### 3. 📺 Suporte Completo a Séries de TV
* Detecção automática de temporadas (`Season 01`, `Season 02`) e episódios (`S01E01`, `S01E02`).
* Modal dedicado para séries com seletor de temporadas e lista de episódios individuais.
* Cada episódio possui botões dedicados para assistir no **Navegador** ou no **VLC**.

### 4. 🔊 Player Web Cinematográfico
* **Controle de Volume com Boost de 200%:** Amplificador dinâmico via Web Audio API para filmes com áudio baixo, permitindo dobrar o volume além do limite convencional de 100%.
* **Legendas Inteligentes:** Renderização de legendas `.srt` externas ou embutidas com suporte a busca de frases dentro do filme e salto temporal.
* **Atalhos de Teclado:**
  * `Espaço` / `K`: Pausar / Reproduzir
  * `Setas Esquerda / Direita` ou `J / L`: Voltar / Avançar 10 segundos
  * `Setas Cima / Baixo`: Aumentar / Diminuir volume
  * `F`: Alternar tela cheia (Fullscreen)
  * `M`: Silenciar (Mute)

### 5. 🚀 Integração de Alta Performance com o VLC Media Player
* Botão **VLC** em todos os cards e modais.
* Abre o filme ou episódio instantaneamente no **VLC Media Player** instalado no seu Windows.
* Ideal para filmes **4K Remux / BluRay pesados** e trilhas de áudio de cinema sem compressão (**DTS-HD, TrueHD, Dolby Atmos, Áudio 5.1 e 7.1**).

### 6. 🏷️ Badges Visuais de Mídia
* **Resolução:** `4K Ultra HD` (dourado), `1080p Full HD` (azul) ou `720p HD`.
* **Áudio:** `DUB` (Dublado), `LEG` (Legendado) ou `DUAL` (Dual Áudio).
* **Legendas:** `CC` (Closed Caption) presente sempre que há legendas disponíveis.

### 7. 📖 Metadados Ricos & Links Externos
* Sinopse detalhada em português (pt-BR).
* Elenco principal e Diretor / Criador.
* Nota e avaliação crítica.
* Botões diretos para consultar a ficha oficial no **TMDb** e **IMDb**.

---

## 📁 Estrutura de Pastas do Projeto

```text
D:\Filmes/
├── Abrir CineLocal.bat                # Inicia a interface no navegador
├── Iniciar Servidor (TV e Celular).bat# Inicia o servidor local na rede
├── Atualizar Catalogo.bat             # Atualiza catálogo e metadados
├── README.md                          # Este guia completo do projeto
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
│   ├── catalogo.js                    # Base de dados compilada em JavaScript
│   ├── .audio_cache.json              # Cache de probes de áudio por timestamp
│   └── bin/
│       └── ffmpeg.exe                 # Binário local do FFmpeg
└── media/
    ├── filmes/                        # Pastas de filmes e franquias
    │   ├── Marvel/                    # Franquia Marvel numerada (#01 a #16)
    │   ├── Batman/
    │   ├── Harry Potter/
    │   ├── Star Wars/
    │   └── [Filmes Avulsos]/
    └── series/                        # Pastas de séries organizadas por temporadas
        ├── Loki/
        ├── WandaVision/
        ├── The Bear/
        └── [Demais Séries]/
```

---

## 🛠️ Como Adicionar Novos Filmes e Séries

1. **Para Filmes Avulsos:**
   * Crie uma pasta em `media/filmes/Nome do Filme (Ano)/`.
   * Coloque o vídeo: `Nome do Filme (Ano) [1080p].ext`.
   * Adicione o poster: salve uma imagem com proporção 2:3 como `poster.jpg` dentro da pasta.
   * Se houver legenda externa, nomeie como `Nome do Filme (Ano) [1080p].srt`.

2. **Para Séries:**
   * Crie a pasta em `media/series/Nome da Serie/`.
   * Crie subpastas de temporada: `Season 01/`, `Season 02/`.
   * Coloque os episódios: `Nome - S01E01.mkv`, `Nome - S01E02.mkv`.
   * Coloque a capa em `media/series/Nome da Serie/poster.jpg`.

3. **Atualize o Catálogo:**
   * Dê dois cliques em **`Atualizar Catalogo.bat`** na raiz.
   * O sistema possui cache inteligente (`.audio_cache.json`) por data de modificação: ele apenas analisa os arquivos novos ou alterados, terminando em poucos segundos!

---

*Desenvolvido com foco em velocidade, autonomia e máxima fidelidade de áudio e vídeo.*
