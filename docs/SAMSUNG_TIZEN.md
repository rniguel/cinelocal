# 📺 Guia de Produção: CineLocal para Samsung Smart TV (Tizen OS)

Este documento é o guia definitivo de engenharia, arquitetura e operação do **CineLocal nativo para Samsung Smart TV (Tizen OS 6.5 a 9.0+)**, empacotado no formato `.wgt`.

---

## 📌 1. Por que o Aplicativo Nativo Substitui o Navegador Web?

| Desafio no Navegador Integrado da Smart TV | Solução com Aplicativo Nativo CineLocal (`.wgt`) |
| :--- | :--- |
| **Limite Crítico de Memória RAM:** Abas do navegador Tizen são restritas a ~300MB–400MB. Catálogos com centenas de filmes e efeitos CSS travam ou fecham a aba inesperadamente. | **Processo Standalone Dedicado:** Executa como aplicativo de sistema independente, com teto de memória alocado pelo SO e sem interface de navegador consumindo recursos. |
| **Perda de Teclas Físicas do Controle:** O navegador da TV consome ou ignora teclas essenciais (Play, Pause, Return, Teclas Coloridas). | **Tizen TV Input Device API (`tizen.tvinputdevice`):** Registro e captura global de todas as teclas físicas do controle remoto original da Samsung. |
| **Decodificação de Vídeo em CPU/Software:** O elemento `<video>` básico tem limites de bitrate e codec na TV. | **Aceleração Samsung AVPlay:** Pronto para ligação direta aos chips de processamento de imagem da Samsung (`webapis.avplay`) para 4K HDR a 60 FPS com áudio pass-through. |
| **Experiência de Uso:** Digitar URLs longas com o controle remoto na TV é desconfortável. | **Descoberta Automática de IP:** O app detecta e conecta ao servidor do computador na rede Wi-Fi sem necessidade de digitação. |

---

## 🏗️ 2. Arquitetura do Aplicativo TV

O aplicativo adota a arquitetura de **Bootstrap Leve + Redirecionamento Dinâmico**:

```text
[Smart TV Samsung]
  │
  ├── 1. Abre o Pacote Nativo Local (.wgt)
  │      ↳ Carrega tizen/index.html
  │      ↳ Registra teclas do controle remoto (tizen.tvinputdevice)
  │
  ├── 2. Descoberta Automática (Auto-Discovery Loop)
  │      ↳ Testa o IP injetado do computador (ex: 192.168.18.5:8000)
  │      ↳ Faz ping em /api/capabilities a cada 2.5s se o servidor estiver iniciando
  │
  └── 3. Redirecionamento com Sessão Exclusiva
         ↳ Redireciona para http://192.168.18.5:8000/app/index.html?tizen=1
         ↳ Habilita aceleração gráfica e navegação total D-Pad
```

Essa arquitetura traz **três grandes vantagens operacionais**:
1. **Atualizações Instantâneas:** Qualquer melhoria feita na interface (`app/index.html`), novos carrosséis ou correções ficam disponíveis na TV no instante em que o arquivo é salvo no PC, sem precisar reinstalar o pacote na TV.
2. **Resiliência a Falhas:** Se o PC for reiniciado ou o IP mudar, a tela de boas-vindas do aplicativo permite redefinir ou reconectar em um clique.
3. **Controle Remoto Direcionado:** O app na TV ganha uma sessão alvo (`cinelocalSessionId`), garantindo que o controle remoto virtual no celular controle exclusivamente a TV.

---

## ⚙️ 3. Estrutura do Pacote Tizen (`config.xml`)

O arquivo `tizen/config.xml` define as propriedades fundamentais exigidas pelo subsistema de empacotamento da Samsung:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<widget xmlns="http://www.w3.org/ns/widgets" 
        xmlns:tizen="http://tizen.org/ns/widgets" 
        id="http://cinelocal.app/CineLocal" 
        version="2.5.0" 
        viewmodes="maximized">
    
    <content src="index.html"/>
    <icon src="icon.png"/>
    <name>CineLocal</name>
    <description>Streaming cinematografico local CineLocal</description>
    
    <!-- REGRA CRÍTICA DO TIZEN: O package deve conter EXATAMENTE 10 caracteres alfanuméricos -->
    <tizen:application id="cinelocal1.CineLocal" package="cinelocal1" required_version="4.0"/>
    
    <!-- Perfil Obrigatório para Smart TV Samsung -->
    <tizen:profile name="tv-samsung"/>
    
    <!-- Permissões de Rede e Controle Remoto -->
    <tizen:privilege name="http://tizen.org/privilege/internet"/>
    <tizen:privilege name="http://tizen.org/privilege/tv.inputdevice"/>
    
    <!-- Configurações de Tela e Hardware Key Events -->
    <tizen:setting screen-orientation="landscape" context-menu="enable" background-support="disable" encryption="disable" install-location="auto" hwkey-event="enable"/>
    
    <!-- Permissão de Acesso à Rede Local -->
    <access subdomains="true" origin="*"/>
</widget>
```

> [!IMPORTANT]
> **Regra dos 10 Caracteres do Tizen:** O atributo `package` dentro de `<tizen:application>` **DEVE ter exatamente 10 caracteres alfanuméricos** (ex: `cinelocal1`). Caso tenha mais ou menos caracteres, ou caso falte a tag `<tizen:profile name="tv-samsung"/>`, o instalador da TV rejeitará o pacote com o erro `Operation not allowed [-4]: Load archive info fail`.

---

## 🔑 4. Ativação do Modo Desenvolvedor na Smart TV Samsung

Para permitir que o computador instale o CineLocal via rede local:

1. Ligue a TV Samsung e verifique se ela e o computador estão na **mesma rede Wi-Fi**.
2. Abra o menu **Smart Hub** e selecione a aba **Apps**.
3. **No controle remoto:**
   * **Controle tradicional com números:** Pressione sequencialmente os números `1` `2` `3` `4` `5`.
   * **Controle moderno (Smart Remote / Solar):** Pressione o botão `123` (teclado virtual de números) e selecione `1`, `2`, `3`, `4`, `5`.
4. Uma janela pop-up de **Developer Mode** aparecerá:
   * Alterne a chave para **ON**.
   * No campo **Host PC IP**, digite o IP local do seu computador (ex: `192.168.18.5`).
   * Clique em **OK**.
5. **Reinicie a Smart TV:** Mantenha o botão **Power** do controle pressionado por cerca de 4 segundos até a tela apagar e aparecer o logotipo da Samsung ao ligar.
6. Ao reabrir o menu de Apps, um banner azul com a indicação **"Developer Mode"** confirmará que o modo está ativo.

---

## 🛡️ 5. Certificados Digitais Samsung & Autorização da TV (DUID)

As Smart TVs Samsung fabricadas a partir de 2016 utilizam o subsistema de segurança **Samsung Certificate Extension**, que exige assinatura digital atrelada ao **DUID (Device Unique Identifier)** da TV:

```text
[Samsung Certificate Manager]
       │
       ├── 1. Author Certificate (author.p12):
       │      Identifica o desenvolvedor (autenticado na Samsung Account).
       │
       └── 2. Distributor Certificate (distributor.p12 + device-profile.xml):
              Contém a autorização oficial com o DUID da TV (ex: CPCPLWH34A24G)
              emitida pela CA da Samsung (svdca.samsungqbe.com).
```

### Como o Perfil Foi Gerado:
1. Abrir o Certificate Manager: `python build_tizen.py --cert`.
2. Criar novo perfil selecionando **Samsung** (não selecionar Tizen genérico).
3. Preencher nome do perfil (`Cinelocal`) e criar a chave de autor fazendo login com a Samsung Account.
4. No passo do Distribuidor, manter como **Public** e marcar a caixinha do dispositivo conectado via SDB (`UN50CU8000GXZD`).
5. **Permit to Install:** O arquivo gerado `device-profile.xml` é automaticamente enviado para `/home/owner/share/tmp/sdk_tools/device-profile.xml` na TV através do comando do gerenciador ou via `build_tizen.py`.

---

## 🎮 6. Mapeamento de Teclas do Controle Remoto Samsung

No ambiente Tizen, os eventos de teclado e controle remoto emitem códigos numéricos específicos:

| Tecla Física do Controle | `keyCode` | `e.key` | Ação no CineLocal |
| :--- | :--- | :--- | :--- |
| **Seta para Cima** | `38` | `ArrowUp` | Foca no item ou linha acima no catálogo |
| **Seta para Baixo** | `40` | `ArrowDown` | Foca no item ou linha abaixo |
| **Seta para a Esquerda**| `37` | `ArrowLeft` | Foca no card anterior no carrossel |
| **Seta para a Direita** | `39` | `ArrowRight` | Foca no próximo card no carrossel |
| **Botão Central / OK** | `13` | `Enter` | Abre detalhes do filme ou inicia reprodução |
| **Voltar (Return / Back)**| `10009`| `Return` | Fecha player de vídeo ou volta para a Home |
| **Play / Pause** | `10252` | `MediaPlayPause`| Alterna reprodução do filme em tela cheia |
| **Botão Vermelho (Red)** | `403` | `ColorF0Red` | Redefine IP na tela inicial do app |

### Registro no Script:
```javascript
if (window.tizen && window.tizen.tvinputdevice) {
  const keys = ['MediaPlay', 'MediaPause', 'MediaPlayPause', '10009', 'Return', 'ColorF0Red'];
  keys.forEach(k => {
    try { tizen.tvinputdevice.registerKey(k); } catch(e){}
  });
}
```

---

## 🛠️ 7. Guia de Operação do Utilitário `build_tizen.py`

Criamos um utilitário de terminal completo para empacotamento, assinatura e deployment:

```powershell
# Execução direta com menu interativo e diagnóstico do ambiente
python build_tizen.py

# Empacotar e instalar automaticamente na TV conectada
python build_tizen.py --install

# Executar o aplicativo diretamente na tela da Smart TV
python build_tizen.py --run

# Conectar a uma TV especificando o endereço IP
python build_tizen.py --connect 192.168.18.204

# Fazer varredura na rede local procurando TVs Samsung na porta 26101
python build_tizen.py --scan

# Abrir o Gerenciador de Certificados Samsung
python build_tizen.py --cert

# Abrir o Gerenciador de Dispositivos (Device Manager)
python build_tizen.py --device-manager
```

---

## 🔍 8. Diagnóstico e Resolução de Problemas Comuns

### 1. `device-profile.xml not found`
* **Causa:** A TV ainda não recebeu o arquivo de autorização com seu DUID.
* **Solução:** No Device Manager da extensão, clique com o botão direito na TV conectada e selecione **"Permit to install applications"**, ou use `python build_tizen.py --install`.

### 2. `Load archive info fail [-4]`
* **Causa:** O ID do pacote em `config.xml` não possui exatamente 10 caracteres ou falta `<tizen:profile name="tv-samsung"/>`.
* **Solução:** Verifique se `package="cinelocal1"` tem 10 caracteres e se o XML está salvo em UTF-8 sem caracteres especiais.

### 3. A TV perde a conexão com o PC (`failed to connect to...`)
* **Causa:** O IP do computador ou da TV mudou no roteador.
* **Solução:** Execute `python build_tizen.py --scan` para reencontrar o IP da TV e execute `python build_tizen.py --connect <NOVO_IP>`.

---

## 🚀 9. Status da Implementação

* [x] Estrutura do widget Tizen Web (`config.xml`, `icon.png`, `index.html`) criada e validada.
* [x] Certificado oficial Samsung gerado e atrelado ao DUID da TV.
* [x] TV autorizada via `Permit to install applications`.
* [x] Pacote `.wgt` assinado e instalado com sucesso na TV (`UN50CU8000GXZD`).
* [x] Auto-descoberta de IP do servidor PC e injeção dinâmica no build.
* [x] Navegação D-Pad do controle remoto Samsung totalmente funcional.
* [x] Pipeline automatizado via `build_tizen.py`.
