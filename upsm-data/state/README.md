# UPSM State Directory

**Version:** 2025-10-18  
**Purpose:** Defines the *structural and computational layer* of the Unified Portfolio System Map (UPSM) — how inputs, derived metrics, modules, and rules interact to generate system behavior (MSI, TTL, KFT, EGI).

---

## 🔹 Directory Role
This directory stores all canonical state definitions and transformation logic.  
It is the single source of truth for **what the system knows** and **how signals propagate**.

| File | Description |
|------|--------------|
| **context.json** | The master schema connecting inputs → derived metrics → modules → rules. |
| **refresh_schedule.json** | Defines update cadence and timing for each data feed. |
| **context_patch_YYYY-MM-DD.json** | Point-in-time snapshots or deltas used for versioned updates. |
| **(optional) auxiliary files** | Submodules or historical regimes (archived MSI/KFT/EGI structures). |

---

## 🔹 Core Concepts

### 1. Inputs
Raw metrics ingested from canonical feeds (see `/upsm-data/feeds/`).  
Each input has:
- a `feed_id` (matching the refresh schedule),
- a value (or null if pending),
- and a defined cadence for refresh.

Example:
```json
"vix_spot": null,
"hyg_pd": null

2. Derived Metrics

Computed transformations used to trigger regime changes:

term_slope = vix3m - vix_spot  
inversion_flag = vix_spot > vix3m  
breadth_spread = spxa50r - spxa200r

Derived metrics exist only here to ensure all calculations are centralized and reproducible.
3. Modules

Logical groupings of signals that adjust MSI and TTL domains:

    Vol/Liq

    Credit

    Energy

    Housing/CRE

    (Optional) Human/Policy, FX Fragility, Private Credit Stress Monitor (PCSM)

Each module lists:

    Inputs it monitors

    Derived metrics it depends on

    Adjustment targets (MSI.Vol_Liq, TTL, etc.)

4. Rules

Conditional statements that translate signal thresholds into regime shifts.
Each rule follows the if / then convention and references only derived metrics or validated inputs.

Example:

{
  "name": "Vol inversion 2d",
  "if": "consecutive_days(inversion_flag, 2)",
  "then": {"MSI.Vol_Liq": "+0.3", "TTL": "-10%"}
}

🔹 MSI / TTL Architecture

MSI (Macro Stress Index):
A five-domain composite measuring system stress (0–5).
Each domain adjusts based on its active rules and contagion multipliers.

TTL (Time-to-Liquidity):
Average number of days required to mobilize liquidity under current conditions.
Rules that increase MSI typically reduce TTL (tighter drift bands).

KFT / EGI (Discipline Metrics):
Defined elsewhere but reference MSI and TTL for dynamic calibration.
🔹 Versioning & Patch Process

    Edit context.json for permanent structural updates.

    Create a dated context_patch_YYYY-MM-DD.json for experimental or time-specific changes.

    Merge and archive patches quarterly once validated.

    Maintain a changelog comment at the top of each file (date, author, change summary).

🔹 Governance & Validation

    Single Source Rule: only /state/context.json defines canonical system logic.

    Downstream Read-Only: dashboards, prompts, and fetchers read from it; they do not write back.

    Change Discipline: any edit must maintain the “one feed → one purpose” principle defined in /feeds/signal_purpose_map.md.

🔹 Cross-References
Directory	Function
/feeds/	Data inputs, purpose map, and refresh cadence.
/prompts/	Behavioral instructions for how to analyze or act.
/state/	Structural definitions for how UPSM logic executes.
🔹 Philosophy

    “The state layer encodes logic, not opinion —
    the feed layer delivers reality —
    the prompt layer interprets both.”

Together, they form an antifragile system: observable, auditable, and self-improving.

Maintainer: Daniel Hill
Last updated: 2025-10-18