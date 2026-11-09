# 🏛️ Arquitetura do Sistema CineLocal

O **CineLocal** é projetado como uma plataforma de streaming doméstico de alto desempenho para redes locais e uso desktop autônomo, combinando um frontend moderno e reativo (*Single Page Application*), um servidor multithread em Python com suporte a HTTP 206 e Server-Sent Events, utilitários de mídia via FFmpeg e um motor de streaming sequencial BitTorrent em Node.js.

---

## 🏗️ Diagrama Geral da Arquitetura

```text
               ┌────────────────────────────────────────────────────────┐
               │           APLICAÇÃO DESKTOP & WEB CINELOCAL            │
               └───────────────────────────┬────────────────────────────┘
                                           │
         ┌─────────────────────────────────┴─────────────────────────────────┐
         ▼                                                                   ▼
┌──────────────────┐                                               ┌──────────────────┐
│  MÍDIAS LOCAIS   │                                               │   BITTORRENT     │
│ (media/filmes &  │                                               │ (Magnet Links &  │
│  media/series)   │                                               │  Multi-Torrents) │
└────────┬─────────┘                                               └────────┬─────────┘
         │                                                                  │
         ▼                                                                  ▼
┌──────────────────┐       ┌────────────────────────┐             ┌──────────────────┐
│atualizar_catalogo│ ◄──── │  Pasta Nativa Vídeos   │             │WebTorrent Engine │
│       .py        │       │(C:\Users\...\Videos e  │             │ (Porta 8888)     │
└────────┬─────────┘       │ ~/Videos/CineLocal)    │             └────────┬─────────┘
         │                 └────────────────────────┘                      │
         ▼                                                                 ▼
┌──────────────────┐                                               ┌──────────────────┐
│   catalogo.js    │                                               │ Stream HTTP 206  │
└────────┬─────────┘                                               │(Buffer de 2 MB)  │
         │                                                                 │
         └───────────────────────────────┬─────────────────────────────────┘
                                         │
                                         ▼
                 ┌────────────────────────────────────────────────┐
                 │       SERVIDOR PYTHON (app/servidor.py)        │
                 │  - HTTP 206 Partial Content (Seek Rápido)      │
                 │  - SSE Remote Controller Hub (/api/remote)     │
                 │  - Remux On-the-Fly MKV/AC3 via FFmpeg         │
                 │  - Dispatch Assíncrono do VLC Media Player     │
                 └───────────────────────┬────────────────────────┘
                                         │
                    ┌────────────────────┴────────────────────┐
                    ▼                                         ▼
     ┌─────────────────────────────┐           ┌─────────────────────────────┐
     │      INTERFACE PRINCIPAL    │           │    CONTROLE REMOTO TOUCH    │
     │      (app/index.html)       │ ◄───────► │     (app/remote.html)       │
     │  - Player Web Cinematográfico│    SSE    │  - D-Pad Tátil com Vibração │
     │  - Central Multi-Torrent    │  Events   │  - Play, Seek, Vol, Legendas│
     │  - D-Pad Foco Smart TV      │           │  - Conexão via QR Code      │
     └─────────────────────────────┘           └─────────────────────────────┘
```

---

## 🖥️ 1. Frontend Unificado (`app/index.html` - Fonte da Verdade)

* **Tecnologia:** HTML5 Semântico, CSS Moderno com Variáveis Customizadas e JavaScript Vanilla puro (sem frameworks pesados, garantindo tempo de carregamento < 50ms).
* **Componentes Centrais:**
  * **Header Dinâmico:** Chips de navegação rápida (*Início*, *Filmes*, *Séries*), contador badge de downloads ativos (*Torrents*), *Surpreenda-me* (🎲 Roleta), atalhos de conexão (*📱 TV / Celular* via QR Code) e busca global instantânea (atalho `/`).
  * **Hero Banner:** Destaque visual com pôster em alta definição, metadados ricos, botões de reprodução rápida, trailer oficial no YouTube e inclusão na lista de favoritos.
  * **Carrosséis Horizontais com Suporte a Touch e Setas:**
    * *⭐ Minha Lista:* Coleção customizada persistida no servidor.
    * *⏱️ Continuar Assistindo:* Retomada sincronizada com tempo restante e barra de progresso.
    * *🔥 Adicionados Recentemente:* Ordenados por data real de gravação em disco.
    * *⚡ Universo Marvel (MCU):* Ordem cronológica canônica com rastreador oficial de 67 títulos.
    * *🏆 Sagas e Franquias:* Agrupamento inteligente de trilogias e coleções.
  * **Player Cinematográfico Avançado:**
    * Implementado sobre `<video>` HTML5 com controles inteligentes que se auto-ocultam.
    * **Web Audio API GainNode:** Super Booster de volume de até 300% para faixas de som baixas.
    * **Remux On-the-Fly:** Transcodificação leve via FFmpeg (`-c:v copy -c:a aac`) para arquivos com contêiner `.mkv` ou áudios incompatíveis com browsers.
    * **Engine de Legendas:** Parser de legendas `.srt` com ajuste de sincronia em tempo real (`G` e `H`).
    * **Integração com VLC:** Botão nativo para abrir mídias pesadas (4K, HDR, Dolby TrueHD, DTS 7.1) no VLC local com 1 clique.

---

## ⚡ 2. Engine Multi-Torrent & Streaming Sequencial (`app/torrent/engine.mjs`)

* **Motor WebTorrent em Node.js (Porta 8888):**
  * **Priorização Sequencial de Peças:** Janela deslizante que prioriza as primeiras 30 peças para buffer imediato de reprodução e as peças finais para índices do contêiner.
  * **Buffer Rápido de 2 MB:** Permite assistir a produções de qualquer tamanho sem esperar o término do download.
  * **Gerenciador Multi-Torrent:** Permite múltiplos downloads concorrentes em background monitorados por cards com velocidade (MB/s), sementes (seeds) e progresso percentual.
  * **Salvamento na Pasta Nativa de Vídeos:** Salva os filmes finalizados na pasta padrão de Vídeos do sistema operacional (`%USERPROFILE%\Videos\CineLocal` no Windows e `~/Videos/CineLocal` no Linux).
  * **Armazenamento Seguro de Cache:** O cache temporário (`.cache`) é alocado na partição do usuário, prevenindo o esgotamento de espaço em discos de mídia secundários.

---

## 📱 3. Hub do Controle Remoto em Tempo Real (`app/remote.html` & SSE)

* **Protocolo Server-Sent Events (SSE):** Comunicação sem latência (< 20ms) entre a Smart TV/computador e smartphones/tablets.
* **Pareamento por QR Code:** Não exige configuração manual de portas nem instalação de aplicativos externos.
* **D-Pad com Haptic Feedback:** Vibração tátil no celular ao navegar pelos menus da Smart TV.
* **Ações Remotas:** Play/Pause, Seek (+/- 10s), Volume (+/- / Mudo), Ajuste de Legendas (+/- 0.1s), Tela Cheia e Voltar.

---

## ⚙️ 4. Servidor de Streaming & APIs (`app/servidor.py`)

* **Python `ThreadingHTTPServer`:** Atende múltiplas requisições simultâneas sem bloqueios.
* **HTTP 206 Partial Content:** Suporte completo a *Byte-Range Requests* para navegação instantânea em qualquer segundo do filme.
* **Junção Transparente de Mídia:** Cria links nativos NTFS / Symlinks entre `media/filmes/Vídeos` e a pasta de Vídeos do SO, unificando a biblioteca física e os downloads em um só catálogo.
* **Direct Stream FFmpeg:** Remuxer de baixa latência com flags `-probesize 1M -analyzeduration 1M -fflags +nobuffer+discardcorrupt`.

---

## 🖥️ 5. Empacotador Desktop Autônomo (`run_desktop.py` & `build_desktop.py`)

* **Processo Unificado sem Fork-Bombs:** `run_desktop.py` executa o servidor em uma thread interna com proteção `multiprocessing.freeze_support()`, garantindo que apenas uma janela dedicada de aplicativo seja aberta.
* **Modo Janela Nativa:** Inicia o Edge/Chrome em modo `--app=http://localhost:8000/app/index.html` maximizado, sem barra de navegação.
* **PyInstaller + Inno Setup:**
  * Compilação via `build_desktop.py` gerando `dist/CineLocal/CineLocal.exe`.
  * Script Inno Setup em `installer/CineLocal.iss` para instaladores formais do Windows (`CineLocal-Setup-v2.5.0.exe`).
  * Script `Iniciar CineLocal Desktop.bat` com desbloqueio automático do Microsoft SmartScreen.
