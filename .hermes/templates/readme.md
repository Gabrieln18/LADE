<!--
templates/readme.md · v0.1.0 · Used by: skills/documentation/repository-docs
Derived from Notion "12 · README — Reference Document". Rules: references/engineering/documentation.md §4 and §7.
- Required sections: Overview, Architecture, Usage, Repository Structure, Testing, Documentation, Project Status, License.
- All other sections are optional: omit them when there is no evidence. Do not leave empty sections.
- Replace every {{PLACEHOLDER}} with evidence or {{TBD}}. Remove this comment and add the traceability header (AGENTS.md §10) as an HTML comment.
- Headings stay in English. Body text follows output_language.
-->

# {{ICON}} {{PROJECT_NAME}}

> {{ONE_LINE_DESCRIPTION}}

{{BADGES}}

---

## 📌 Overview

{{WHAT_THIS_COMPONENT_IS_AND_WHY_IT_EXISTS}}

### What it does

- {{RESPONSIBILITY_01}}
- {{RESPONSIBILITY_02}}

### What it does not do

- {{OUT_OF_SCOPE_01}}
- {{OUT_OF_SCOPE_02}}

---

## 🎯 Purpose <!-- optional -->

{{PROBLEM_THIS_COMPONENT_SOLVES}}

| Goal | Description |
|------|-------------|
| {{GOAL_01}} | {{DESCRIPTION}} |

---

## 🏗️ Architecture

{{SHORT_ARCHITECTURAL_SUMMARY}}

```mermaid
{{MERMAID_DIAGRAM_ONLY_IF_IT_CLARIFIES}}
```

| Component | Responsibility |
|-----------|----------------|
| {{COMPONENT_01}} | {{RESPONSIBILITY}} |

**Architecture source of truth:** {{ARQ_ID_OR_LINK}}

---

## 🧩 Core Concepts <!-- optional -->

| Concept | Description |
|---------|-------------|
| {{CONCEPT_01}} | {{DESCRIPTION}} |

---

## 🔌 Interfaces & Integration <!-- optional -->

{{HOW_THIS_COMPONENT_COMMUNICATES_WITH_OTHERS}}

| Interface | Direction | Purpose |
|-----------|-----------|---------|
| {{INTERFACE_01}} | {{INBOUND_OR_OUTBOUND}} | {{PURPOSE}} |

**Contract source of truth:** {{IF_OR_EVT_ID_OR_LINK}}

---

## 💻 Usage

Examples MUST use real, supported APIs. Mark anything else `# Conceptual example`.

### Installation

```bash
{{INSTALL_COMMAND}}
```

### Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `{{VARIABLE_01}}` | Yes | — | {{DESCRIPTION}} |

### Basic usage

```{{LANGUAGE}}
{{VERIFIED_USAGE_EXAMPLE}}
```

---

## 🛠️ Technology Stack <!-- optional -->

| Category | Technology | Purpose |
|----------|------------|---------|
| {{CATEGORY}} | {{TECHNOLOGY}} | {{PURPOSE}} |

**Stack source of truth:** {{STK_ID_OR_LINK}}

---

## 📁 Repository Structure

```text
{{PROJECT_ROOT}}/
├── {{DIRECTORY_01}}/
├── tests/
├── docs/
└── README.md
```

| Directory | Responsibility |
|-----------|----------------|
| `{{DIRECTORY_01}}/` | {{DESCRIPTION}} |

---

## 🧪 Testing

```bash
{{TEST_COMMAND}}
{{LINT_COMMAND}}
{{FORMAT_COMMAND}}
```

{{TEST_STRATEGY_IN_ONE_OR_TWO_SENTENCES}}

---

## 📊 Observability <!-- optional -->

| Signal | Technology | Purpose |
|--------|------------|---------|
| {{LOGS_METRICS_TRACES}} | {{TECHNOLOGY}} | {{PURPOSE}} |

---

## 🔐 Reliability & Security <!-- optional -->

- {{PRINCIPLE_01}}

---

## 🌐 Execution Models <!-- optional -->

{{MODULAR_CLOUD_AND_OR_MONOLITHIC_EDGE}}

---

## 🔗 Related Components <!-- optional -->

| Component | Relationship |
|-----------|--------------|
| {{COMPONENT}} | {{RELATIONSHIP}} |

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| {{DOCUMENT_ID_OR_LINK}} | {{PURPOSE}} |

---

## 🚧 Project Status

| Attribute | Value |
|-----------|-------|
| Maturity | {{Experimental \| Alpha \| Beta \| Stable \| Production \| Deprecated}} |
| Version | {{VERSION}} |
| Maintainer | {{TEAM_OR_OWNER}} |

**Known limitations:** {{LIMITATION_01}}

---

## 🤝 Contributing <!-- optional -->

See [CONTRIBUTING.md](./CONTRIBUTING.md).

## 📦 Release & Versioning <!-- optional -->

Semantic Versioning 2.0.0. History in [CHANGELOG.md](./CHANGELOG.md).

---

## 📄 License

{{LICENSE_INFORMATION}}