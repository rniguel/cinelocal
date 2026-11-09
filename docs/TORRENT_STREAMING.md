# ⚡ Streaming de Torrent & Gerenciador Multi-Torrent

O **CineLocal** incorpora uma engine avançada de streaming sequencial de torrents e magnet links baseada em **WebTorrent**, proporcionando uma experiência de cinema sob demanda similar ao *Stremio* ou *Popcorn Time*, totalmente integrada à sua biblioteca de filmes.

---

## 🎯 Visão Geral & Filosofia

Ao contrário dos clientes de torrent tradicionais que baixam blocos aleatórios pela rede para maximizar o compartilhamento, o motor do CineLocal utiliza **estratégia sequencial de peças**:

```text
[Magnet Link / Hash]
        │
        ▼
 [WebTorrent Engine (app/torrent/engine.mjs)]
        │
        ├── Prioridade Máxima nas Primeiras 30 Peças (Cabeçalho/Moov Container)
        ├── Prioridade Alta nas Peças Finais (Tabelas de Indexação Seek)
        └── Download Contínuo dos Demais Blocos Sequenciais
        │
        ▼
   Porta 8888 (HTTP 206 Partial Content Stream)
        │
        ├──► [Modo 1: VLC 1-Clique] ──────► 4K/HDR / DTS 7.1 / TrueHD Nativo
        │
        └──► [Modo 2: Navegador Web] ─────► Remux On-the-Fly via FFmpeg (-c:v copy -c:a aac)
```

1. **Reprodução Imediata (Buffer de 2 MB):** Não é necessário esperar o download de arquivos pesados de 2 GB a 20 GB. Assim que os metadados são resolvidos e cerca de **2 MB** são recebidos, o player inicia a reprodução.
2. **Compatibilidade Universal de Codecs:**
   - **VLC 1-Clique:** Arquivos com contêiner `.mkv`, áudio surround de cinema (**AC3, EAC3, DTS-HD, Dolby Atmos**) ou HDR abrem instantaneamente no VLC com legendas sincronizadas.
   - **Player Web Integrado:** Se assistido pelo navegador, o servidor remuxa o contêiner em tempo real via FFmpeg sem re-encodar o vídeo (`-c:v copy`), com consumo de CPU quase nulo.
3. **Salvamento na Pasta Nativa de Vídeos:**
   - No Windows: `C:\Users\<Usuario>\Videos\CineLocal\<Filme (Ano)>\`
   - No Linux: `~/Videos/CineLocal/<Filme (Ano)>/`
   - No macOS: `~/Movies/CineLocal/<Filme (Ano)>/`

---

## 🛠️ Como Usar a Central de Torrents

### 1. Adicionando um Magnet Link
1. Na barra superior do CineLocal, clique no botão **⚡ Torrents**.
2. Na aba **➕ Adicionar Magnet Link**, cole o seu link `magnet:?xt=urn:btih:...` ou hash do torrent.
3. O CineLocal detectará automaticamente o nome, ano e consultará o **Cinemeta / TMDb** para exibir a capa oficial, sinopse e nota antes de iniciar.
4. Escolha como deseja assistir:
   - **Assistir no Navegador:** Dispara o player cinematográfico do CineLocal.
   - **🚀 Assistir no VLC:** Dispara o VLC instalado no computador conectando diretamente ao stream HTTP local.

### 2. Gerenciador Multi-Torrent (Fila de Downloads)
Acesse a aba **📥 Downloads Ativos** para monitorar todos os downloads simultâneos em segundo plano:
* **Cards em Tempo Real:** Título, ano, poster, quantidade de sementes ativas (seeds) e velocidade atual de download (ex: `14.2 MB/s`).
* **Barra de Progresso:** Percentual baixado e tamanho total formatado.
* **Ações Rápidas por Item:**
  * **▶ Navegador:** Retoma ou inicia o player web na tela.
  * **🚀 VLC:** Transmite o stream para o VLC Player.
  * **💾 Salvar:** Move o arquivo finalizado diretamente para sua pasta de Vídeos permanente e indexa no catálogo.
  * **🗑️ Remover:** Encerra as conexões no enxame, desaloca a memória e remove o item instantaneamente da fila.

---

## ⚙️ Arquitetura Técnica & Endpoints

O motor Node.js roda na porta `8888` e é gerenciado automaticamente pelo `servidor.py`:

| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/api/torrent/health` | Verifica a integridade e quantidade de torrents ativos. |
| `GET` | `/api/torrent/list` | Retorna a lista detalhada de todos os torrents na fila com progresso e velocidade. |
| `GET` | `/api/torrent/status?infoHash=...` | Retorna o status individual de um torrent específico ou do mais recente. |
| `POST` | `/api/torrent/start` | Adiciona um novo magnet link à fila (`{ magnet, title, year, poster }`). |
| `POST` | `/api/torrent/remove` | Encerra e remove o torrent da fila (`{ infoHash, deleteCache }`). |
| `POST` | `/api/torrent/save` | Copia o vídeo baixado para a pasta permanente `Videos/CineLocal`. |
| `GET` | `/webtorrent/:infoHash/:file` | Stream HTTP 206 sequencial de blocos de vídeo. |

---

## 💡 Dicas de Desempenho

* **Sementes (Seeds):** Prefira magnet links com pelo menos 10 a 20 sementes ativas para garantir streaming fluído sem pausas para buffering.
* **Espaço em Disco:** O cache temporário (`.cache`) e os filmes salvos ficam localizados na partição do usuário (drive `C:` no Windows), garantindo dezenas ou centenas de gigabytes livres para downloads sem travar unidades secundárias.
