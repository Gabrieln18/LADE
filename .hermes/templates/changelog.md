<!--
templates/changelog.md · v0.1.0 · Used by: skills/documentation/changelog
Derived from Notion "CHANGELOG.MD". Standards: Keep a Changelog, Semantic Versioning 2.0.0.
- Only include sections that have entries. Newest release first. Dates are ISO 8601 (UTC).
- Section labels below are PT-BR (default output_language). Mapping and EN names: skills/documentation/changelog/SKILL.md.
- Entry format: one line, effect for the user, suffix (LADE-YYYYMMDD-NNN[, ADR-NNNN]).
- Breaking: start with **BREAKING:**, add the ADR and a migration hint.
- Remove this comment and add the traceability header (AGENTS.md §10) as an HTML comment at the top of the file.
-->

# Changelog

Todas as alterações notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado no [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

---

## [Unreleased]

### 🚀 Adicionado
- {{USER_FACING_DESCRIPTION}} ({{TASK_ID}})

### 🔄 Alterado
- **BREAKING:** {{DESCRIPTION}}. Migração: {{ONE_LINE_HINT}}. ({{TASK_ID}}, {{ADR_ID}})

### ⚠️ Descontinuado
- {{DESCRIPTION}}. Remoção prevista para {{VERSION_OR_DATE}}. ({{TASK_ID}})

### 🗑️ Removido
- {{DESCRIPTION}} ({{TASK_ID}})

### 🐛 Corrigido
- {{DESCRIPTION}} ({{TASK_ID}})

### 🔒 Segurança
- {{IMPACT_DESCRIPTION_WITHOUT_EXPLOIT_DETAILS}} ({{TASK_ID}})

---

## [{{VERSION}}] - {{DATE}}

### 🚀 Adicionado
- {{DESCRIPTION}} ({{TASK_ID}})

---

[Unreleased]: {{REPOSITORY_URL}}/compare/v{{LATEST_VERSION}}...HEAD
[{{VERSION}}]: {{REPOSITORY_URL}}/releases/tag/v{{VERSION}}