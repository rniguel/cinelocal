# 🤝 Guia de Contribuição para o CineLocal

Agradecemos imensamente pelo seu interesse em contribuir com o **CineLocal**! Seja corrigindo um bug, adicionando um recurso visual inovador, melhorando a documentação ou otimizando a reprodução de mídia em Smart TVs e navegadores, toda contribuição é muito bem-vinda.

Este documento estabelece o fluxo de trabalho (**Git Flow**), convenções de código, ciclo de abertura de Pull Requests e como resolver Issues de maneira padronizada.

---

## 📌 Sumário

1. [Código de Conduta & Princípios](#-código-de-conduta--princípios)
2. [Estratégia de Branches (Git Flow)](#-estratégia-de-branches-git-flow)
3. [Como Escolher ou Criar uma Issue](#-como-escolher-ou-criar-uma-issue)
4. [Passo a Passo para Contribuir](#-passo-a-passo-para-contribuir)
   * [1. Fork e Clonagem](#1-faça-o-fork-e-clone-o-repositório)
   * [2. Configuração de Remotes](#2-configure-o-upstream-remoto)
   * [3. Criação da Branch](#3-crie-uma-branch-a-partir-de-develop)
   * [4. Regras Fundamentais do CineLocal](#4-regras-fundamentais-de-desenvolvimento)
   * [5. Padrão de Commits](#5-padrão-de-commits-conventional-commits)
   * [6. Publicação e Pull Request](#6-envie-suas-alterações-e-abra-o-pull-request)
5. [Processo de Revisão e Merges](#-processo-de-revisão-e-merges)
6. [Estrutura do Projeto & Onde Modificar](#-estrutura-do-projeto--onde-modificar)

---

## 🧭 Princípios & Regras Fundamentais

Antes de escrever qualquer linha de código, guarde estas três regras de ouro do ecossistema:

1. **Preservação Absoluta de Mídia:** Nunca escreva rotinas ou scripts que excluam arquivos de vídeo (`.mkv`, `.mp4`, `.avi`, etc.) sem autorização explícita do usuário.
2. **Sincronização da Interface Web (Regra de Ouro):**
   * O arquivo `app/generate_netflix_ui.py` é a fonte oficial da interface `app/index.html`.
   * Sempre que for alterar HTML, CSS ou JavaScript do frontend, aplique a modificação no gerador `app/generate_netflix_ui.py` e execute:
     ```bash
     python app/generate_netflix_ui.py
     ```
   * Isso regenera `app/index.html` e mantém ambos em perfeita sincronia.
3. **Compatibilidade & Codificação:**
   * Todos os arquivos de texto e código Python devem ser salvos com codificação **UTF-8**.
   * Respeite caminhos multiplataforma com barras normais `/` nos links web e `os.path.normpath` em sistemas operacionais Windows/Linux.

---

## 🌿 Estratégia de Branches (Git Flow)

Adotamos um modelo baseado em **Git Flow simplificado**, com foco em estabilidade para releases e agilidade para novas colaborações:

```text
main       ────────────────────────●───────────────● (v1.1.0 - Release Estável)
                                  /               /
develop    ────────●─────────────●───────●───────● (Integração Contínua)
                    \           /         \     /
feature              ●─────────●           ●───● (Sua Feature / Fix)
```

| Branch | Finalidade | Regras de Merge |
|---|---|---|
| **`main`** | Versão estável em produção. Todo commit aqui deve ser funcional e pronto para uso final. | Apenas merges aprovados originados de `develop` ou `hotfix/`. |
| **`develop`** | Branch principal de integração. É aqui que novas funcionalidades e correções se encontram. | **Branch alvo padrão de todos os Pull Requests da comunidade.** |
| **`feature/*`** | Criação de novas ferramentas, telas, melhorias de UX e novos endpoints. | Criada a partir de `develop`, mesclada de volta em `develop`. |
| **`fix/*`** | Correção de defeitos ou problemas de estabilidade identificados em desenvolvimento. | Criada a partir de `develop`, mesclada de volta em `develop`. |
| **`hotfix/*`** | Correções emergenciais e pontuais para quebras críticas encontradas na `main`. | Criada a partir de `main`, mesclada em `main` e em `develop`. |
| **`docs/*`** | Melhorias em documentação, guias, tutoriais ou traduções. | Criada a partir de `develop`, mesclada em `develop`. |

---

## 🎯 Como Escolher ou Criar uma Issue

### Para Reportar um Bug ou Propor Melhoria
1. Acesse a aba **[Issues](https://github.com/rniguel/cinelocal/issues)** do repositório oficial.
2. Verifique se o problema ou sugestão já não foi reportado por outra pessoa.
3. Caso não exista, clique em **New Issue**:
   * Utilize um título claro e descritivo (ex: `[BUG] Legenda .srt externa dessincronizada no Chrome`).
   * Explique os passos para reproduzir, comportamento esperado, versão do navegador e sistema operacional.

### Para Resolver uma Issue Existente
1. Escolha uma issue que não possua responsáveis atribuídos (fique de olho nas tags `good first issue` ou `help wanted`).
2. Deixe um comentário na issue dizendo: *"Olá! Gostaria de trabalhar nesta issue."*
3. Assim que alinhado, inicie o passo a passo descrito abaixo.

---

## 🚀 Passo a Passo para Contribuir

### 1. Faça o Fork e Clone o Repositório

Faça um Fork do projeto no GitHub clicando no botão **Fork** no canto superior direito do repositório oficial: `https://github.com/rniguel/cinelocal`.

Em seguida, clone o seu fork para a sua máquina local:

```bash
git clone https://github.com/SEU_USUARIO/cinelocal.git
cd cinelocal
```

### 2. Configure o Upstream Remoto

Adicione o repositório original como `upstream` para poder sincronizar atualizações futuras facilmente:

```bash
git remote add upstream https://github.com/rniguel/cinelocal.git
git fetch upstream
```

### 3. Crie uma Branch a partir de `develop`

> [!IMPORTANT]
> **Nunca** crie branches de novas features ou correções a partir da `main`. Certifique-se de basear seu trabalho na branch `develop`.

```bash
# Vá para a develop e certifique-se de que está atualizada
git checkout develop
git pull upstream develop

# Crie sua branch com um nome semântico
# Exemplo para features:
git checkout -b feature/suporte-tema-escuro-oled

# Ou exemplo para correções:
git checkout -b fix/audio-sem-som-firefox
```

#### Convenção de Nomenclatura de Branches:
* `feature/<nome-curto>`: Novas telas, filtros, módulos ou botões.
* `fix/<nome-curto>`: Correções de bugs ou falhas.
* `docs/<nome-curto>`: Documentação, manuais e README.
* `refactor/<nome-curto>`: Limpeza e melhoria estrutural de código sem alterar regra de negócio.

---

### 4. Regras Fundamentais de Desenvolvimento

1. **Testando a Aplicação Localmente:**
   Execute o servidor local para validar suas alterações:
   ```bash
   python app/servidor.py
   ```
   Acesse no navegador: `http://localhost:8000`.

2. **Se você alterou a Interface (HTML, CSS ou JavaScript do Frontend):**
   * Edite **sempre** o gerador `app/generate_netflix_ui.py`.
   * Regenere o `app/index.html`:
     ```bash
     python app/generate_netflix_ui.py
     ```
   * Verifique o resultado no navegador e certifique-se de que não há erros no console (`F12`).

3. **Se você adicionou regras de metadados:**
   * Atualize os dicionários correspondentes em `app/metadata_db.py`.

---

### 5. Padrão de Commits (Conventional Commits)

Utilizamos o padrão **Conventional Commits** para manter o histórico de alterações limpo e legível:

```text
<tipo>(<escopo opcional>): <descrição sucinta em minúsculas>
```

#### Tipos Permitidos:
* `feat`: Nova funcionalidade para o usuário final.
* `fix`: Correção de um bug.
* `docs`: Alterações exclusivamente em documentação.
* `style`: Formatação, pontuação, espaçamento (sem alteração de lógica).
* `refactor`: Refatoração de código que não altera comportamento público nem corrige bugs.
* `perf`: Mudança no código que melhora a performance.
* `test`: Adição ou correção de testes automatizados.
* `chore`: Atualização de tarefas de build, gitignore, dependências auxiliares.

#### Exemplos Práticos:
```bash
git commit -m "feat(player): adicionar atalho para pular abertura do episodio"
git commit -m "fix(remote): corrigir atraso no comando de volume pelo celular"
git commit -m "docs(contributing): documentar fluxo de git flow e pull request"
```

---

### 6. Envie suas Alterações e Abra o Pull Request

1. Envie a sua branch para o seu repositório remoto no GitHub (Fork):
   ```bash
   git push -u origin feature/suporte-tema-escuro-oled
   ```

2. Vá até o repositório oficial no GitHub. Você verá um aviso sugerindo a criação do Pull Request.
3. Clique em **Compare & pull request**.
4. **MUITO IMPORTANTE - Seleção da Branch Base:**
   * **Base Repository:** `rniguel/cinelocal` | **base:** `develop` ⬅️ *(Certifique-se de que o alvo é `develop`, NÃO a `main`)*
   * **Head Repository:** `SEU_USUARIO/cinelocal` | **compare:** `feature/suporte-tema-escuro-oled`

5. **Preencha a Descrição do PR:**
   * Forneça um resumo claro do que foi implementado ou corrigido.
   * Conecte a Issue correspondente para fechamento automático:
     ```text
     Closes #12
     # ou
     Fixes #45
     ```
   * Se envolver interface gráfica, anexe capturas de tela ou GIFs antes/depois.

---

## 🔍 Processo de Revisão e Merges

1. **Revisão pelos Mantenedores:**
   * O código será avaliado em relação à coerência, estabilidade, ausência de efeitos colaterais e aderência às regras do projeto.
   * Comentários ou pedidos de ajuste podem ser feitos diretamente nas linhas de código do PR.

2. **Ajustes:**
   * Caso melhorias sejam solicitadas, basta fazer os ajustes no seu repositório local e fazer novo `git push` na mesma branch. O Pull Request será atualizado automaticamente!

3. **Merge em `develop`:**
   * Uma vez aprovado, seu PR será mesclado na branch `develop`.

4. **Release e Merge para a `main`:**
   * Periodicamente, o mantenedor reúne as melhorias validadas em `develop`, testa o conjunto e faz o merge de `develop` para a `main`, gerando uma nova versão (tag de release estável).

---

## 🗂️ Estrutura do Projeto & Onde Modificar

```text
CineLocal/
├── CONTRIBUTING.md            # Este guia de colaboração
├── README.md                  # Apresentação do projeto e manual de uso
├── GEMINI.md                  # Regras operacionais do projeto para IAs
├── docs/                      # Documentação técnica e aprofundada
│   ├── ARQUITETURA.md         # Detalhes da arquitetura do player e servidor
│   └── GUIA_MIDIA.md          # Formatos suportados, codecs e legendas
├── app/
│   ├── generate_netflix_ui.py # ⚠️ FONTE MESTRE DA UI (edite aqui para mexer na interface)
│   ├── index.html             # Gerado automaticamente por generate_netflix_ui.py
│   ├── remote.html            # Interface web do controle remoto para smartphones
│   ├── servidor.py            # Servidor HTTP local em Python com rotas de API
│   ├── atualizar_catalogo.py  # Scanner de pastas e montagem do catalogo.js
│   └── metadata_db.py         # Base de dados de sinopses, diretores e elencos
└── media/                     # Pastas reservadas para mídias locais do usuário
```

---

<p align="center">
  Obrigado por ajudar a tornar o <strong>CineLocal</strong> uma plataforma incrível para todos! 🍿🚀
</p>
