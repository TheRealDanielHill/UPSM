# UPSM Prompt Library

**Version:** 2025-10-18  
**Purpose:** This directory defines the *behavioral layer* of the Unified Portfolio System Map (UPSM) — the reusable prompt blueprints that describe **how** the system should think, analyze, and act in different contexts.

---

## 🔹 Directory Role
Prompts in this folder act as *operational playbooks* for the Human–AI partnership.  
Each file is a structured “task schema” that standardizes recurring workflows across UPSM domains.

| Mode | Description | Example Prompt |
|------|--------------|----------------|
| **Exploration** | Pseudo-integration + red-team of external sources (YouTube, news, policy, macro commentary). | `Analyze_News_Source.txt` |
| **Audit** | Runs scheduled data refresh and MSI/TTL recalculation using canonical feeds. | `Fast_Pass_Audit.txt` |
| **Reflection** | Adversarial or red-team review of theses, trades, or assumptions. | `Red_Team_Template.txt` |
| **Rebalance** | Integrates promoted signals into the UPSM core (MSI/TTL/Tile updates). | `UPSM_Integration_Request.txt` |

---

## 🔹 Registry
All prompt files are indexed in [`prompt_registry.json`](./prompt_registry.json).

Each registry entry includes:
- `id`: canonical name used for invocation.
- `file`: filename within this directory.
- `purpose`: one-line human description.
- `invocation_context`: which mode triggers it (Exploration, Audit, Reflection, Rebalance).
- `outputs`: expected response artifacts (cards, tables, ledger entries, etc.).
- `affects`: whether the prompt changes MSI, TTL, or ledger entries.
- `tags`: quick semantic identifiers for retrieval.

---

## 🔹 Usage
Prompts are invoked contextually by ID, e.g.:

run prompt: fast_pass_audit


or

analyze with prompt: analyze_news_source


Each file begins with a `# UPSM Prompt Spec` header that declares its metadata for model recognition.

---

## 🔹 Maintenance & Versioning
- **Add new prompts** here as your workflows evolve.  
- **Update the registry** whenever a new file is added or removed.  
- **Quarterly Review:** prune redundant prompts and tag entries as `"core"`, `"experimental"`, or `"archived"`.  
- **Cross-referencing:** Prompts that directly affect MSI/TTL logic should reference the current `/upsm-data/state/context.json` structure.

---

## 🔹 Philosophy
> *“The prompt library teaches the system how to think —  
>  the state directory tells it what to know —  
>  the ledger remembers what we’ve learned.”*

This separation keeps the UPSM antifragile: each component can evolve independently without corrupting the others.

---

**Maintainer:** Daniel Hill  
**Last updated:** 2025-10-18