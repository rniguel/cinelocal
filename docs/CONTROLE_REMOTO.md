# 📱 Controle Remoto Virtual para Smart TV & Mobile

O **CineLocal** inclui um ecossistema de controle remoto virtual em tempo real sem a necessidade de instalar aplicativos externos na Google Play ou App Store. Qualquer celular ou tablet na mesma rede Wi-Fi se transforma em um controle touch interativo.

---

## 🚀 Como Conectar com Emparelhamento por Aba (Issue #19)

Para evitar interferência quando múltiplas telas ou abas estão abertas na mesma casa (por exemplo, alguém assistindo na TV da sala enquanto outra pessoa usa o monitor do quarto), o CineLocal implementa o sistema de **Sessão Alvo (Target Session)**:

1. **Abra o QR Code na TV ou Aba que Deseja Controlar:**
   * Clique no ícone de **📱 TV / Celular** na barra superior ou acesse o menu **"Controle Remoto no Celular"**.
2. **Escaneie com a Câmera do Celular:**
   * O QR Code gerado contém a assinatura exclusiva daquela aba:
     ```text
     http://<IP-DO-COMPUTADOR>:8000/remote?target=cinese_abc123xyz
     ```
3. **Controle Exclusivo e Direcionado:**
   * O celular salva o identificador da tela emparelhada.
   * Todos os comandos de navegação, volume, play e pause enviados pelo celular são despachados **apenas para a TV ou aba correspondente**, ignorando outras instâncias do CineLocal abertas na rede local.

---

## 🎮 Funcionalidades do Controle Remoto (`/remote`)

### 1. D-Pad Tátil com Vibração (Haptic Feedback)
* **Setas Direcionais (`↑`, `↓`, `←`, `→`):** Navegue pelos carrosséis, menus e cartazes de filmes na tela grande da TV ou monitor.
* **Botão Central (OK / Selecionar):** Abre a ficha técnica ou inicia a reprodução do título focado.
* **Feedback Háptico:** O celular vibra levemente a cada toque confirmando o comando (disponível em dispositivos móveis compatíveis com `navigator.vibrate`).

### 2. Controles de Reprodução e Mídia
* **Play / Pause:** Alterna a reprodução do filme ou série em tela cheia.
* **Avanço e Retrocesso (-10s / +10s):** Pula ou repete cenas rapidamente.
* **Controle de Volume (- / + / Mudo):** Ajusta o volume do player em passos de 5% ou silencia o áudio.
* **Alternar Tela Cheia (Fullscreen):** Expande ou minimiza o vídeo na TV.
* **Fechar / Voltar:** Fecha o player ou sai de modais abertos na tela principal.

### 3. Sincronia de Legendas na Palma da Mão
* Permite adiantar ou atrasar a legenda ativa em tempo real (`-0.1s` / `+0.1s`), ideal para quando a legenda externa estiver ligeiramente dessincronizada com o diálogo.

---

## 🏗️ Protocolo de Comunicação (SSE + REST com Target Routing)

A comunicação entre a Smart TV / Computador e o Celular ocorre através de uma arquitetura leve, sem websockets pesados:

```text
[Celular /remote?target=cinese_123] ── POST /api/remote/action (target: cinese_123) ──► [servidor.py]
                                                                                               │
[Smart TV (sessão cinese_123)] ◄──── SSE Stream /api/remote/events (filtra e executa) ─────────┤
[Outro PC (sessão cinese_999)] ◄──── SSE Stream /api/remote/events (ignora comando) ───────────┘
```

* **Server-Sent Events (`/api/remote/events`):** Reconexão nativa e transparente no navegador, baixíssimo consumo de bateria e latência inferior a 50ms.
* **Fallback Polling:** Para navegadores ou ambientes restritos onde SSE não está disponível, há fallback automático de long-polling a cada 500ms.
* **Badge de Tela Ativa:** A interface do controle remoto exibe no topo o identificador da tela conectada, permitindo limpar ou alternar o pareamento a qualquer momento.
