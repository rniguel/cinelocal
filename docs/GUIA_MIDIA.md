# 🎥 Guia de Mídia, Codecs e Nomenclatura

Este guia orienta sobre como organizar, nomear e otimizar arquivos de vídeo, capas e legendas para obter a melhor experiência no **CineLocal**.

---

## 📁 1. Padrões de Nomenclatura

### Filmes Avulsos (Standalones)
Crie uma pasta com o nome e o ano do filme. Dentro dela, coloque o vídeo, o poster e eventuais legendas:

```text
media/filmes/
└── Interestelar (2014)/
    ├── Interestelar (2014) [1080p BluRay].mkv
    ├── Interestelar (2014) [1080p BluRay].srt
    └── poster.jpg
```

### Franquias e Sagas
Para franquias, crie a pasta da saga e subpastas numeradas com dois dígitos para definir a ordem de exibição no catálogo:

```text
media/filmes/Marvel/
├── 01 - Capitão América - O Primeiro Vingador (2011)/
│   ├── Capitão América - O Primeiro Vingador (2011) [1080p].mkv
│   └── poster.jpg
├── 02 - Os Vingadores (2012)/
│   ├── Os Vingadores (2012) [1080p].mkv
│   └── poster.jpg
└── 06 - Deadpool 2 (2018)/
    ├── Deadpool 2 (2018) [720p].mp4
    ├── Deadpool 2 (2018) [720p].forced.srt
    └── poster.jpg
```

### Séries de TV
Séries devem ser organizadas por pastas de temporadas:

```text
media/series/Loki/
├── poster.jpg
├── Season 01/
│   ├── Loki - S01E01.mkv
│   ├── Loki - S01E01.srt
│   └── Loki - S01E02.mkv
└── Season 02/
    ├── Loki - S02E01.mkv
    └── Loki - S02E01.srt
```

---

## 🏷️ 2. Tags no Nome do Arquivo

O scanner do CineLocal identifica metadados a partir do nome do arquivo:
* **Resolução:** Inclua tags como `[4K]`, `[2160p]`, `[1080p]` ou `[720p]` no nome do vídeo. Isso ativa automaticamente as badges de resolução nos cards.
* **Ano:** Mantenha sempre o ano de lançamento entre parênteses: `(2024)`.
* **Versão Estendida:** Se o arquivo ou pasta contiver `Versão Estendida` ou `Extended`, a interface destacará essa edição.

---

## 🔊 3. Codecs de Áudio: Navegador vs VLC

| Codec de Áudio | Reprodução no Navegador | Reprodução no VLC | Recomendação |
|---|---|---|---|
| **AAC (Estéreo / 5.1)** | ✅ Suporte Nativo Perfeito | ✅ Perfeito | Navegador ou VLC |
| **MP3** | ✅ Suporte Nativo | ✅ Perfeito | Navegador |
| **AC3 / E-AC3 (Dolby Digital)** | ⚠️ Depende do hardware/navegador | ✅ Excelente com 5.1 real | Navegador ou VLC |
| **DTS / DTS-HD Master Audio** | ❌ Não suportado pelo Chrome | ✅ Fidelidade máxima de cinema | **Usar botão VLC** |
| **TrueHD / Dolby Atmos** | ❌ Não suportado pelo Chrome | ✅ Fidelidade máxima sem perdas | **Usar botão VLC** |

> **Dica:** Para filmes pesados com áudio DTS ou TrueHD, você tem duas opções:
> 1. Clicar no botão **VLC** no CineLocal para assistir imediatamente com qualidade total.
> 2. Rodar o script `app/otimizar_audio_web.bat`, que cria uma cópia rápida da trilha de áudio em AAC sem reencodar o vídeo.

---

## 💬 4. Legendas (`.srt`)

* **Nome do Arquivo:** A legenda externa deve ter o mesmo nome base do vídeo:
  * Vídeo: `Filme (2024) [1080p].mkv`
  * Legenda: `Filme (2024) [1080p].srt`
* **Legendas Forçadas:** Se for uma legenda para partes em idioma estrangeiro de um filme dublado, adicione `.forced.srt`:
  * `Filme (2024) [1080p].forced.srt`
* **Legendas embutidas:** Arquivos `.mkv` com legendas internas são detectados automaticamente pelo FFmpeg e sinalizados com a badge `CC` no card.

---

## 🔄 5. Como Trocar um Filme por uma Versão de Qualidade Superior

Se você baixou uma versão melhor (ex: substituindo uma versão 720p por 1080p ou 4K):
1. Acesse a pasta do filme em `media/filmes/Nome do Filme (Ano)/`.
2. **Exclua o arquivo de vídeo antigo** de qualidade inferior.
3. Cole o novo arquivo de alta qualidade.
4. Se houver legenda externa `.srt`, renomeie-a para bater com o novo nome do arquivo.
5. Dê dois cliques em **`Atualizar Catalogo.bat`**.
6. O scanner invalidará o cache daquele filme pelo `mtime`, recalculará o tamanho, resolução e trilhas de áudio, mantendo seu `poster.jpg` e sinopse 100% preservados!
