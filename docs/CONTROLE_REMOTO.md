# 📱 Controle Remoto Virtual para Smart TV & Mobile

O **CineLocal** inclui um ecossistema de controle remoto virtual em tempo real sem a necessidade de instalar aplicativos externos na Google Play ou App Store. Qualquer celular ou tablet na mesma rede Wi-Fi se transforma em um controle touch interativo.

---

## 🚀 Como Conectar

1. **Inicie o Servidor:**
   Execute `Iniciar Servidor (TV e Celular).bat` (Windows) ou `./"Iniciar Servidor (TV e Celular).sh"` (Linux/macOS).
2. **Abra o QR Code na TV ou Computador:**
   Clique no ícone de **📱 TV / Celular** na barra de navegação superior do CineLocal.
3. **Escaneie com a Câmera do Celular:**
   Aponte a câmera do celular para o QR Code ou digite diretamente o endereço no navegador do celular:
   ```text
   http://<IP-DO-COMPUTADOR>:8000/remote
   ```
4. **Pronto!** O controle conecta automaticamente via **Server-Sent Events (SSE)** em menos de 100ms.

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

## 🏗️ Protocolo de Comunicação (SSE + REST)

A comunicação entre a Smart TV / Computador e o Celular ocorre de maneira bidirecional através de uma arquitetura leve e resiliente:

```text
[Celular /remote] ──── HTTP POST /api/remote/action ────► [servidor.py]
                                                                 │
[Smart TV /index.html] ◄── SSE Stream /api/remote/events ────────┘
```

* **Sem WebSocket Pesado:** Utiliza **HTTP Server-Sent Events (`/api/remote/events`)**, que tem reconexão nativa automática pelo navegador, baixíssimo consumo de bateria e funciona mesmo em Smart TVs mais antigas com navegadores web limitados.
* **Ações Suportadas:**
  * `play_pause`, `seek_forward`, `seek_backward`
  * `volume_up`, `volume_down`, `mute`
  * `nav_up`, `nav_down`, `nav_left`, `nav_right`, `nav_select`, `nav_back`
  * `fullscreen`, `sub_sync_delay`, `sub_sync_advance`
