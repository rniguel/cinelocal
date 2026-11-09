# 🏪 Guia Oficial: Publicação na Loja de Aplicativos Samsung Smart TV (Tizen App Store)

Este documento detalha o processo, requisitos técnicos, políticas de homologação e passos práticos para publicar o **CineLocal** na loja oficial da Samsung (**Samsung Apps TV / Seller Office**).

---

## 📌 1. Visão Geral da Samsung TV Store

A Samsung Smart TV opera com o portal oficial **Samsung Apps TV Seller Office** ([seller.samsungapps.com/tv](https://seller.samsungapps.com/tv)). Através dele, desenvolvedores cadastram, submetem e distribuem pacotes `.wgt` para mais de 200 milhões de televisores ativos globalmente.

Existem dois modelos principais de distribuição:
1. **Distribuição Pública Global (Public App Store):** Disponível para qualquer usuário baixar direto pela TV. Exige homologação de QA e conformidade rigorosa de conteúdo.
2. **Grupo de Usuários Fechado (User Group / Beta Testing):** Permite distribuir o app automaticamente para até **50 Smart TVs** (através do DUID ou contas Samsung cadastradas), **sem necessidade de aprovação da esteira pública de QA da Samsung**. Excelente para uso próprio, amigos e família.

---

## 📋 2. Requisitos Obrigatórios de Homologação (Samsung QA Checklist)

Para que um aplicativo seja aprovado pela equipe de QA da Samsung, ele **deve** atender a estes testes obrigatórios:

### A. Navegação e Controle Remoto
* **Tecla Voltar (Return / Back Key - `10009`):**
  * Quando pressionada dentro de um modal ou player, deve fechá-lo.
  * Quando pressionada na tela principal (Home), **DEVE exibir um diálogo nativo de confirmação**: *"Deseja sair do CineLocal?"* com opções *Sim* e *Não*.
  * Ao escolher *Sim*, o app deve invocar:
    ```javascript
    tizen.application.getCurrentApplication().exit();
    ```
  * *Atenção:* Se o botão Return fechar o app abruptamente na Home sem confirmação, a Samsung **rejeita** a submissão.

### B. Desempenho e Memória (Performance Benchmarks)
* **Tempo de Inicialização (Cold Boot):** O app deve carregar a primeira tela visível em **menos de 4 segundos**.
* **Consumo de Memória RAM:** Não pode ultrapassar 300MB no pico de reprodução.
* **Sem Vazamento de Memória (Memory Leak):** O app é submetido a testes de stress de navegação contínua por 60 minutos sem congelamento.

### C. Ciclo de Vida e Segundo Plano (App Lifecycle)
* Se o usuário alternar para a entrada HDMI ou abrir o menu da TV durante a reprodução, o app deve disparar evento de pausa imediata e silenciar o áudio.

---

## ⚖️ 3. Política de Conteúdo e Legalidade (Atenção Crítica)

> [!WARNING]
> **Políticas Rígidas da Samsung Store:** A Samsung é extremamente rigorosa quanto a direitos autorais e pirataria. Qualquer aplicativo que ofereça busca, download ou streaming de torrents públicos de filmes protegidos por direitos autorais é **sumariamente banido e rejeitado**.

### Como os Grandes Players Operam (O Modelo Plex / Jellyfin):
Para ser aceito na loja oficial, o aplicativo deve se posicionar estritamente como um **"Player de Mídia Pessoal / Nuvem Doméstica"**:
* **Versão para a Loja Oficial:** O pacote submetido deve focar exclusivamente na reprodução dos arquivos locais do computador (`media/filmes/`), catalogação inteligente, capas do TMDb e sincronia de legendas.
* O motor de WebTorrent pode ser mantido como módulo experimental opcional acessível apenas via configuração avançada no servidor local do usuário, ou distribuído via sideload / Developer Mode.

---

## 🚀 4. Passo a Passo para Submeter no Samsung Seller Office

### Passo 1: Cadastro no Samsung Developers
1. Acesse [developer.samsung.com](https://developer.samsung.com/) e crie uma conta gratuita.
2. Acesse o **Samsung Apps TV Seller Office**: [seller.samsungapps.com/tv](https://seller.samsungapps.com/tv).
3. Conclua o cadastro de desenvolvedor individual ou corporativo.

### Passo 2: Cadastro do Aplicativo
1. No painel do Seller Office, clique em **"Create App"**.
2. Preencha as informações cadastrais:
   * **App Name:** CineLocal
   * **Category:** Video / Media
   * **Languages:** Português (Brasil), Inglês, Espanhol.
   * **Description:** *"Central multimídia doméstica para reprodução em alta definição do seu catálogo pessoal na rede local."*

### Passo 3: Preparação dos Assets Visuais
* **Ícone Principal:** Formato PNG, `512 x 512 px`, fundo opaco (sem cantos transparentes).
* **Screenshots da Interface:** Mínimo de 4 imagens em resolução Full HD (`1920 x 1080 px`), formato PNG ou JPG (sem mockups ou bordas de TV).
* **Política de Privacidade:** Link para uma página web pública descrevendo como os dados locais são mantidos no dispositivo.

### Passo 4: Assinatura com Certificado Samsung Partner / Public
1. Gerar o pacote `.wgt` assinado com o perfil oficial (como fizemos com `build_tizen.py`).
2. Fazer o upload do arquivo `dist/CineLocal.wgt`.
3. O validador automático do Seller Office inspecionará o `config.xml` em tempo real.

### Passo 5: Teste Beta (User Group) antes da Loja Pública
Antes de pedir a homologação global:
1. Vá na aba **"Self-Test / User Group"**.
2. Adicione o DUID da sua TV e das TVs de quem quiser testar.
3. O app fica disponível **instantaneamente** na aba de Apps daquelas televisões cadastradas!

---

## 🛠️ 5. Checklist Técnico Pré-Submissão

- [x] Package ID de exatamente 10 caracteres (`cinelocal1`).
- [x] Elemento `<tizen:profile name="tv-samsung"/>` presente no `config.xml`.
- [x] Ícone `512x512` em `tizen/icon.png`.
- [x] Suporte total a navegação D-Pad do controle físico.
- [x] Perfil de alta performance ativado (`body.is-tv` sem blurs pesados).
- [ ] Diálogo nativo de confirmação de saída ao pressionar `Return` na Home.
- [ ] Política de Privacidade hospedada em URL pública.
