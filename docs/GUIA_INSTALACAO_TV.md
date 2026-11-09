# 📺 Guia Rápido: Como Instalar o CineLocal na sua Smart TV Samsung em 3 Passos

Este guia prático ensina como colocar o aplicativo **CineLocal** na sua Smart TV Samsung sem precisar de pen drive ou lojas de terceiros, usando apenas a sua rede Wi-Fi local.

---

## ⚡ Passo 1: Ativar o Modo Desenvolvedor na TV (Apenas 1 Vez)

1. Ligue a TV Samsung e verifique se ela está conectada no **mesmo Wi-Fi do seu computador**.
2. Abra o menu **Smart Hub** (Home) e vá na aba **Apps**.
3. **No controle remoto:**
   * **Se o controle tiver números:** Pressione seguidamente os números `1` `2` `3` `4` `5`.
   * **Se o controle for moderno (sem números):** Pressione o botão `123` (teclado virtual de números) e selecione `1`, `2`, `3`, `4`, `5`.
4. Uma janela pop-up de **Developer Mode** vai abrir:
   * Mude a chavinha para **ON**.
   * No campo **Host PC IP**, digite o IP do seu computador (ex: `192.168.18.5`).
   * Clique em **OK**.
5. **Reinicie a TV:** Segure o botão **Power** do controle remoto por 4 segundos até a tela apagar e aparecer o logotipo da Samsung ao ligar.
6. Pronto! A TV já está autorizada a receber o aplicativo.

---

## 🚀 Passo 2: Instalar com 1 Clique pelo Computador

No terminal do seu computador (na pasta do CineLocal), basta executar:

```powershell
python build_tizen.py --install
```

O script faz tudo sozinho:
1. Detecta sua Smart TV na rede local via SDB.
2. Empacota e assina o aplicativo com o certificado oficial.
3. Envia o pacote `.wgt` para a TV e inicializa o app na tela grande!

---

## 🍿 Passo 3: Usar e Assistir

1. Na TV, o ícone do **CineLocal** já aparece na sua barra de Apps!
2. Ao abrir na TV, o aplicativo busca o servidor do seu computador e **conecta automaticamente**.
3. Use o controle remoto original da Samsung para navegar pelos filmes com as **setas direcionais (▲ ▼ ◄ ►)** e aperte **OK** para dar play em tela cheia!

---

> [!TIP]
> **Dicas Úteis:**
> * Para abrir o app na TV direto pelo terminal do PC: `python build_tizen.py --run`
> * Se mudar de rede Wi-Fi, execute: `python build_tizen.py --scan`
