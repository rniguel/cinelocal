# 📺 Guia de Desenvolvimento: CineLocal para Samsung Smart TV (Tizen OS)

Este documento descreve os padrões arquiteturais, pré-requisitos, configurações e passos necessários para transformar o **CineLocal** em um aplicativo nativo empacotado para Smart TVs Samsung equipadas com o sistema **Tizen OS** (`.wgt`), eliminando a lentidão e as limitações de memória do navegador integrado.

---

## 📌 1. Por que o Navegador da TV é Lento?

| Limitação do Navegador da Smart TV | Solução com Aplicativo Nativo Tizen (`.wgt`) |
| :--- | :--- |
| **Limite Estrito de Memória RAM:** Abas do navegador Tizen são restritas a ~300MB–500MB, engasgando com DOMs extensos e blur de CSS. | **Alocação Standalone:** O app roda em processo dedicado com maior teto de memória e sem o consumo da interface de abas do navegador. |
| **Decodificação de Vídeo Ineficiente via `<video>`:** O elemento de vídeo HTML5 básico não aproveita a aceleração do processador de imagem. | **Samsung AVPlay (`webapis.avplay`):** Conecta-se diretamente aos chips DSP de hardware da televisão para decodificação suave de **4K, HDR e 60 FPS**. |
| **Falta de Teclas de Mídia no Controle:** O navegador intercepta teclas ou não reconhece Play, Pause, Voltar (Return) e Color Keys. | **Tizen TV Input Device API:** Registro total de todas as teclas físicas do controle remoto Samsung via `tizen.tvinputdevice`. |

---

## ⚙️ 2. Estrutura do Pacote Tizen (`config.xml`)

Todo aplicativo web Tizen exige um arquivo `config.xml` em sua raiz:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<widget xmlns="http://www.w3.org/ns/widgets" 
        xmlns:tizen="http://tizen.org/ns/widgets" 
        id="http://cinelocal.app/CineLocal" 
        version="2.5.0" 
        viewmode="fullscreen">
    
    <content src="index.html"/>
    <icon src="icon.png"/>
    <name>CineLocal</name>
    
    <tizen:application id="W2O345xxxx.CineLocal" package="W2O345xxxx" required_version="4.0"/>
    
    <!-- Permissões de Rede e Controle Remoto -->
    <tizen:privilege name="http://tizen.org/privilege/internet"/>
    <tizen:privilege name="http://tizen.org/privilege/tv.inputdevice"/>
    
    <!-- Política de Acesso Externo (WARP) -->
    <access subdomains="true" origin="*"/>
</widget>
```

---

## 🎬 3. Player Nativo via Samsung AVPlay (`webapis.avplay`)

No ambiente Tizen, o script `$WEBAPIS/webapis/webapis.js` fica disponível globalmente. Para máxima performance:

```html
<!-- No cabeçalho do index.html -->
<script type="text/javascript" src="$WEBAPIS/webapis/webapis.js"></script>
```

```javascript
// Exemplo de reprodução acelerada por hardware
if (window.webapis && window.webapis.avplay) {
  const streamUrl = "http://192.168.0.10:8000/api/stream?path=" + encodeURIComponent(mediaPath);
  
  webapis.avplay.open(streamUrl);
  webapis.avplay.setDisplayRect(0, 0, 1920, 1080);
  
  webapis.avplay.setListener({
    onbufferingstart: () => showLoading(true),
    onbufferingcomplete: () => {
      showLoading(false);
      webapis.avplay.play();
    },
    oncurrentplaytime: (timeMs) => updateSeekBar(timeMs / 1000),
    onerror: (err) => console.error("AVPlay Error:", err),
    onplaybackcomplete: () => onMovieFinished()
  });

  webapis.avplay.prepareAsync(() => {
    webapis.avplay.play();
  });
}
```

---

## 🔑 4. Como Ativar o Developer Mode na Samsung Smart TV

Para instalar e testar o CineLocal diretamente pela rede Wi-Fi local:

1. Ligue a Smart TV Samsung.
2. Abra o menu **Smart Hub** e selecione a aba **Apps**.
3. No painel de Apps, pressione a sequência numérica **`1 2 3 4 5`** no controle remoto (ou use o teclado virtual de números).
4. Na janela pop-up que aparecer:
   * Alterne **Developer Mode** para **ON**.
   * Insira o **Endereço IP do Computador** onde o servidor CineLocal ou Tizen Studio está rodando (ex: `192.168.0.15`).
   * Clique em **OK**.
5. Reinicie a Smart TV (desligue segurando o botão Power por 4 segundos até aparecer a logo da Samsung).
6. Um aviso indicando **"Develop Mode"** aparecerá no topo da tela.

---

## 📦 5. Pré-Requisitos e Pendências Técnicas

1. **Samsung Certificate Manager (Grátis):**
   * É necessário criar um perfil de certificado (Author Certificate e Distributor Certificate com o DUID da TV) para assinar pacotes `.wgt`.
2. **Tizen Studio ou Tizen CLI:**
   * Ferramentas oficiais da Samsung para empacotar (`tizen package -t wgt`) e enviar para a TV (`tizen install -n CineLocal.wgt -t <device_ip>`).
3. **Perfil "TV Lite" na Interface Web:**
   * Desativar sombras pesadas e `backdrop-filter: blur()` em TVs mais antigas.
   * Paginação virtual de linhas do catálogo para garantir consumo de RAM inferior a 150MB.
