# 🧰 LADE (Hermes)

Ambiente de agentes especializados que transforma tarefas de engenharia em artefatos revisados e governados para o Lattinus Code.

<p align="center">
  <img src="./assets/hermes_agent_wordmark_colored_hero_banner.png" alt="LADE (Hermes)" width="100%" />
</p>

<p align="center">
  <strong>User Task → Orchestrator → Agents → Artifact → Policy Gates → Reviewer → Lattinus Code</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-early--stage-orange" alt="Status" />
  <img src="https://img.shields.io/badge/structure-v2.0-blue" alt="Structure" />
  <img src="https://img.shields.io/badge/lang-Markdown-informational" alt="Language" />
  <img src="https://img.shields.io/badge/framework-TBD-lightgrey" alt="Framework" />
  <img src="https://img.shields.io/badge/tests-evals%20(planned)-lightgrey" alt="Testing" />
  <img src="https://img.shields.io/badge/quality-reviewer%20gate-green" alt="Quality" />
</p>

<p align="center">
  <a href="#-overview">Overview</a> •
  <a href="#-responsibilities">Responsibilities</a> •
  <a href="#-architectural-position">Architecture Position</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-core-concepts">Core Concepts</a> •
  <a href="#-interface-and-contract-model">Interfaces</a> •
  <a href="#-technology-stack">Tech Stack</a> •
  <a href="#-repository-structure">Repository</a> •
  <a href="#-getting-started">Getting Started</a> •
  <a href="#-development">Development</a> •
  <a href="#-testing">Testing</a> •
  <a href="#-security">Security</a> •
  <a href="#-observability">Observability</a> •
  <a href="#-deployment-models">Deployment</a> •
  <a href="#-documentation">Documentation</a>
</p>

> ⚠️ **Fase inicial (estrutura v2.0).** Nomes, agentes, skills e workflows podem mudar. Seções marcadas com `TBD` serão detalhadas conforme o LADE tomar forma.

---

## 📌 Overview

O **LADE (Hermes)** é um ambiente multi-agent, organizado no diretório `.hermes/`, que recebe tarefas de engenharia, distribui o trabalho entre agentes especializados e entrega artefatos revisados.

O componente pertence à **camada de desenvolvimento assistido por agentes** do ecossistema Lattinus e provê **orquestração, skills, references, policies, memory e revisão** como capacidades centrais.

Seu objetivo principal é **gerar código e artefatos técnicos com padronização, rastreabilidade e revisão obrigatória**, permitindo que **mantenedores e colaboradores do Lattinus** entreguem para o **Lattinus Code** com mais consistência e menos retrabalho.

> TODO: confirmar a expansão da sigla **LADE**.

### Architectural Context

O LADE não executa a plataforma: ele **produz** artefatos (design, ADR, código, revisão) que alimentam o Lattinus Code. O conhecimento de domínio vem de `references/`, derivado do [Notion Lattinus](https://app.notion.com/p/Lattinus-2f673eebda2f80d7973fc08ef9558a2e).

O componente é projetado para permanecer **modular, auditável e governado por policies**, mantendo fronteiras explícitas com os demais componentes da plataforma.

```
┌─────────────────────────────┐        ┌──────────────────────┐
│  Notion Lattinus (contexto) │───────▶│  references/         │
└─────────────────────────────┘        └──────────┬───────────┘
                                                  │
┌─────────────┐   task.md   ┌─────────────────────▼──────────┐   artefatos   ┌───────────────┐
│  Humano     │────────────▶│        LADE (.hermes/)         │──────────────▶│ Lattinus Code │
└─────────────┘             └────────────────────────────────┘               └───────────────┘
```

---

## 🎯 Responsibilities

| Agente | Responsabilidade |
|--------|------------------|
| `orchestrator` | Interpreta a tarefa, roteia, delega via `task.md` e fecha o `project-state` |
| `architect` | Design de sistemas, ADRs e análise de dependências |
| `software-engineer` | Implementação (Python, Go, APIs, testes, refactoring) |
| `data-engineer` | Ingestão, pipelines, data contracts e data quality |
| `geospatial-engineer` | Raster/vector, CRS, Earth Observation, Dask/Xarray, Sedona |
| `ai-engineer` | Design de agentes, multi-agent, avaliação e integração com LLMs |
| `devops-sre` | Containers, observability, deployment e security |
| `reviewer` | Revisão, veredito, `lessons.md` e dono de `documentation/*` |

Cada agente declara em seu `AGENTS.md`: `skills`, `references`, `policies`, `workflows` e `can_write`.

**Fora de escopo:** execução em produção da plataforma Lattinus.

---

## 🧭 Architectural Position

- **Camada:** desenvolvimento assistido por agentes.
- **Upstream:** tarefas humanas (`templates/task.md`) e contexto do Lattinus (`references/`).
- **Downstream:** Lattinus Code (contrato de saída em `references/lattinus-code.md`).

---

## 🏗️ Architecture

```
 USER TASK
     │
     ▼
 ORCHESTRATOR ──(templates/task.md)──▶ AGENTE(S)
                                          │
                                          ▼
                                      ARTEFATO
                                          │
                                          ▼
                              POLICY GATES (policies/)
                                          │
                                          ▼
                                      REVIEWER
                                          │
                      ┌───────────────────┼───────────────────┐
                      ▼                   ▼                   ▼
                    PASS              REWORK             ESCALATE
                      │            (máx. 2 ciclos)        (humano)
                      ▼
               MEMORY UPDATE
                      │
                      ▼
               LATTINUS CODE
```

---

## 💡 Core Concepts

- **Precedência:** `SOUL.md` raiz → `AGENTS.md` raiz → agente. O mais específico vence, **exceto `policies/`, que sempre prevalecem**.
- **Manifest:** cada agente carrega sob demanda apenas o que declara.
- **Fonte única:** conhecimento em `references/`, templates em `templates/`, sem cópias.
- **Reviewer loop:** máximo de 2 ciclos de `REWORK`, depois `ESCALATE` para humano.
- **Memory:** `decisions.md` só recebe ADR aprovado; `lessons.md` é escrito pelo Reviewer; `open-questions.md` aceita qualquer agente.

---

## 🔌 Interface and Contract Model

| Contrato | Arquivo | Descrição |
|----------|---------|-----------|
| Handoff | `templates/task.md` | Obrigatório para delegar entre agentes |
| Revisão | `templates/review.md` | Checklist + veredito `PASS \| REWORK(agente, motivo) \| ESCALATE` |
| Decisão | `templates/adr.md` | Registro de decisões de arquitetura |
| Saída | `references/lattinus-code.md` | Repo, branch, PR e definição de pronto |

---

## 🧰 Technology Stack

`TBD` — a definir quando o runtime for escolhido. Hoje o repositório é composto por arquivos Markdown (`SOUL.md`, `AGENTS.md`, `SKILL.md`, etc.).

---

## 📁 Repository Structure

| Pasta | Propósito | Quem escreve |
|-------|-----------|--------------|
| `config/` | Permissões e ferramentas/MCPs | Humanos |
| `agents/` | `SOUL.md` e manifest (`AGENTS.md`) por agente | Humanos |
| `skills/` | Catálogo único de skills (`SKILL.md`) | Humanos |
| `references/` | Fonte única de conhecimento | Humanos |
| `memory/` | Estado, decisões, convenções, lições, dúvidas | Agentes (ver `memory/README.md`) |
| `workflows/` | Sequência de agentes, gates e aprovações humanas | Humanos |
| `templates/` | Único local dos templates | Humanos |
| `policies/` | Gates bloqueantes (safety, dependencies, git, documentation) | Humanos |
| `evals/` | Golden tasks e relatórios por versão | Humanos / Reviewer |

Na raiz: `AGENTS.md` (regras globais para agentes), `SOUL.md` (identidade e valores) e este `README.md` (para humanos).

---

## 🚀 Getting Started

1. Descreva a tarefa usando `templates/task.md`.
2. Escolha o workflow em `workflows/` (ou deixe o Orchestrator rotear).
3. Acompanhe o artefato, o veredito do Reviewer e as atualizações em `memory/`.

> `TBD`: forma de execução e local dos artefatos, quando o runtime estiver definido.

---

## 🛠️ Development

- **Novo agente:** criar `agents/<nome>/` com `SOUL.md`, `AGENTS.md` (manifest) e `references/`; registrar em `agents/orchestrator/references/routing.md`.
- **Nova skill:** criar `skills/<categoria>/<nome>/SKILL.md` e adicioná-la ao manifest dos agentes que a usam.
- **Novo workflow:** criar `workflows/<nome>.md` com agentes, entradas/saídas, gates e aprovações humanas.

---

## 🧪 Testing

Golden tasks em `evals/golden-tasks/` (`by-agent/` e `by-workflow/`); resultados por versão de SOUL/skill em `evals/reports/`.

> `TBD`: como executar os evals.

---

## 🔒 Security

Regras bloqueantes em `policies/` (`safety.md`, `dependencies.md`, `git.md`, `documentation.md`). Permissões por agente em `config/permissions.md`. As policies sempre prevalecem sobre qualquer instrução de agente.

---

## 📊 Observability

`TBD`

---

## ☁️ Deployment Models

`TBD`

---

## 📚 Documentation

| Documento | Local |
|-----------|-------|
| Regras globais para agentes | `AGENTS.md` |
| Regras de memória | `memory/README.md` |
| Contexto Lattinus (snapshot de `AAAA-MM-DD`) | `references/lattinus.md` |
| Fonte do contexto | [Notion Lattinus](https://app.notion.com/p/Lattinus-2f673eebda2f80d7973fc08ef9558a2e) |

**Versão:** v2.0 (2026-11-03) · Changelog: `TBD` (`CHANGELOG.md`)