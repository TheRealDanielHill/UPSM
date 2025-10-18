# UPSM — Signal Purpose Map
**Purpose:** a single, human-readable legend for every feed.  
**Rule:** one feed → one purpose → one module variable. No cross-writes.

_Last updated: 2025-10-18_

---

## 0) Conventions (read me first)

- **Feed ID:** canonical key used in `/feeds/refresh_schedule.json` and `/state/context.json`.
- **Primary Use:** the one job this feed does in UPSM (avoid duplication).
- **Derived Metrics:** what we compute from the feed (if any).
- **MSI Domain:** which MSI domain it informs — `Vol/Liq`, `Credit`, `Energy`, `Housing/CRE`, `Human/Policy`, `FX Fragility`.
- **TTL Impact:** how it tightens/loosens the Time-to-Liquidity bands when the rule trips.
- **Tripwires:** exact if/then triggers we reference (mirrors `/state/context.json` rules).
- **Notes:** brief context; keep plain-language.

> Jargon key:  
> **Term inversion** = VIX > VIX3M (near-term risk higher than 3-month).  
> **Breadth** = % of stocks above moving averages (how many are participating).  
> **Premium/discount** (P/D) = ETF price vs NAV (liquidity stress proxy).  
> **Timespread** = difference between futures maturities (curve shape = supply/demand).

---

## 1) Volatility & Breadth

| Feed ID | Source | Primary Use | Derived Metrics | MSI Domain | TTL Impact | Tripwires | Notes |
|---|---|---|---|---|---|---|---|
| `vix_spot` | FRED: VIXCLS | Near-term market risk gauge | `inversion_flag = vix_spot > vix3m` ; `term_slope = vix3m - vix_spot` | Vol/Liq | Tighten −10% when inverted (2 closes) | **Vol inversion 2d** → `MSI.Vol_Liq +0.3` | Use as canonical VIX close; no other VIX source writes state. |
| `vix3m` | Cboe: VIX3M (VXV) | Term structure anchor | with `vix_spot` → `term_slope`, `inversion_flag` | Vol/Liq | with rule above | Same as above | Use Cboe for VIX3M only (avoid duplicate spot sources). |
| `breadth_spxa50r` | StockCharts | Breadth tile (fast) | `breadth_spread = spxa50r - spxa200r` | Vol/Liq | Tighten −10% | **Spread ≤ −15 pp** → `MSI.Vol_Liq +0.3` | Use % above 50-DMA as “participation” proxy. |
| `breadth_spxa200r` | StockCharts | Breadth tile (slow) | `breadth_spread` with 50R | Vol/Liq | With rule above | With rule above | 200-DMA captures structural participation. |
| `breadth_ndxa50r` | StockCharts | NASDAQ breadth color only | — | Vol/Liq (color) | None | None (narrative only) | Do **not** wire to rules; use for context. |

---

## 2) Credit & Liquidity

| Feed ID | Source | Primary Use | Derived Metrics | MSI Domain | TTL Impact | Tripwires | Notes |
|---|---|---|---|---|---|---|---|
| `hyg_pd` | iShares HYG P/D % | Bond-ETF liquidity stress | `credit_avg_pd_5d` with `lqd_pd` | Credit | Tighten −10% | **|avg P/D| ≥ 0.50% (5d)** → `MSI.Credit +0.2` | Use P/D as liquidity proxy (avoid mixing with perf ratio). |
| `lqd_pd` | iShares LQD P/D % | IG ETF liquidity stress | `credit_avg_pd_5d` | Credit | With rule above | With rule above | Keep method identical to HYG. |
| `ici_flows` | ICI weekly | Systemic flow confirmation | 4-wk delta (computed downstream) | Vol/Liq (color) | None unless rule added | (Optional) 4-wk Δ < −50% → `+0.2` | Keep as **confirmation**, not primary trigger. |

*Optional (not wired by default):*  
- Loan ETF flows (SRLN/BKLN), LSTA loan price, gating events → narrative or future rule additions.

---

## 3) Energy (WTI curve & cracks)

| Feed ID | Source | Primary Use | Derived Metrics | MSI Domain | TTL Impact | Tripwires | Notes |
|---|---|---|---|---|---|---|---|
| `wti_front` | CME/Barchart CL | Front leg for 1–3M spread | `energy_spread_front = wti_1m - wti_front` | Vol/Liq | Tighten −25% when energy rule trips | **Front < −0.10 AND Long < −0.80 (5d)** → `MSI.Vol_Liq +0.3` | Sample once daily at US open for consistency. |
| `wti_1m` | CME/Barchart CL+1M | 1-3M spread | `energy_spread_front` | Vol/Liq | With rule above | With rule above | — |
| `wti_12m` | CME/Barchart CL+12M | 12–24M spread | `energy_spread_long = wti_24m - wti_12m` | Vol/Liq | With rule above | With rule above | — |
| `wti_24m` | CME/Barchart CL+24M | 12–24M spread | `energy_spread_long` | Vol/Liq | With rule above | With rule above | Longer-dated balance. |
| `rbob_crack` | crack proxy | Refining margin stress | — | Vol/Liq (Energy tile) | None | **RBOB < $10 (10d)** → add HAL put spreads | Use direction; no MSI delta by default. |
| `ulsd_crack` | crack proxy | Distillate margin stress | — | Vol/Liq (Energy tile) | None | **ULSD < $20 (10d)** → add HAL put spreads; de-beta | Same handling as RBOB. |

---

## 4) Housing / CRE

| Feed ID | Source | Primary Use | Derived Metrics | MSI Domain | TTL Impact | Tripwires | Notes |
|---|---|---|---|---|---|---|---|
| `mba_apps` | MBA weekly | Demand pulse | — | Credit | Via rule below | **If falling to new cycle low** (contextual) | Narrative + confirm with price-based tiles. |
| `itb_ret20d` | ITB | Homebuilders stress | 20D return (pre-computed) | Credit | Tighten −10% when red with other tiles | **ITB ≤ −8% in 10D** + builder guide-downs → `MSI.Credit +0.2` | Combine with qualitative headlines. |
| `kre_ret20d` | KRE | Regional banks proxy | 20D return | Credit | Tighten −15% when extreme | **KRE ≤ −10% in 20D** with CRE headlines → `MSI.Credit +0.3–0.4` | Proxy for CRE stress. |
| `cmbs_bbb_oas` | index/vendor | Credit spread stress | vs 6-mo avg | Credit | Tighten −15% when red | **OAS > +100 bps vs 6-mo avg** → `MSI.Credit +0.3` | Requires reliable series/vendor. |

---

## 5) Derived Metrics (single source of truth)

| Name | Definition | Feeds Used | Notes |
|---|---|---|---|
| `term_slope` | `vix3m - vix_spot` | `vix_spot`, `vix3m` | Negative = steeper near-term risk. |
| `inversion_flag` | `vix_spot > vix3m` | same | Use 2-close rule for signals. |
| `breadth_spread` | `breadth_spxa50r - breadth_spxa200r` | breadth feeds | ≤ −15 pp = unhealthy participation. |
| `credit_avg_pd_5d` | `rolling_mean(abs(hyg_pd), abs(lqd_pd), 5)` | HYG/LQD P/D | Captures sustained ETF liquidity stress. |
| `energy_spread_front` | `wti_1m - wti_front` | WTI | < −$0.10 = near-term glut/weakness. |
| `energy_spread_long` | `wti_24m - wti_12m` | WTI | < −$0.80 = long-dated weakness. |

---

## 6) Rules (pointer to `/state/context.json`)

- **Vol inversion 2d:** if `consecutive_days(inversion_flag, 2)` → `MSI.Vol_Liq +0.3`, `TTL −10%`.
- **Breadth spread stress:** if `breadth_spread ≤ −15` → `MSI.Vol_Liq +0.3`, `TTL −10%`.
- **Bond ETF liquidity stress:** if `credit_avg_pd_5d ≥ 0.5` → `MSI.Credit +0.2`, `TTL −10%`.
- **Energy backwardation stress:** if `energy_spread_front < −0.10` **AND** `energy_spread_long < −0.80 (5d)` → `MSI.Vol_Liq +0.3`, `TTL −25%`, add SPX/QQQ put spreads funded by overwrites.
- **Crack spread weakness:** if `rbob_crack < 10` **OR** `ulsd_crack < 20 (10d)` → add HAL put spreads; de-beta Energy.
- **CRE credit stress:** if `cmbs_bbb_oas > +100` **OR** `kre_ret20d ≤ −10` → `MSI.Credit +0.3`, `TTL −15%`, add VIX call spreads.

---

## 7) Governance

- **Change requests:** add/edit here first (PR), then update `refresh_schedule.json` and `context.json`.
- **One-owner rule:** each feed has a “maintainer” (your future self counts). The maintainer confirms purpose alignment on change.
- **No duplicate purposes:** if two feeds claim the same purpose, resolve before merge. Keep “one feed → one purpose.”

---

## 8) Changelog

- **2025-10-18:** Initial map created. Canonicalized VIX (FRED), VIX3M (Cboe), breadth via StockCharts, HYG/LQD P/D for liquidity, WTI spreads split (front & long), and Housing/CRE tiles formalized.

## 9) MSI Fast-Pass Checklist (Human–AI Co-Pilot Edition)

> Use this as the live routine before each trading week or when major data prints update.

**Step 1 — Refresh Timing**
- Confirm which feeds in `refresh_schedule.json` are due (`daily_close`, `weekly`, `intraday`).
- For any missing or stale values, fetch once (VIX, breadth, WTI spreads, HYG/LQD).
- Do *not* re-fetch intraday feeds unless TTL < 10 d.

**Step 2 — Compute Derived Metrics**
- `term_slope`, `inversion_flag`, `breadth_spread`, `credit_avg_pd_5d`,  
  `energy_spread_front`, `energy_spread_long`.

**Step 3 — Evaluate Tripwires**
- Check every rule in `/state/context.json` → mark triggered ✅ or not.
- Apply MSI and TTL deltas immediately in-chat.

**Step 4 — Update Headers**
- `MSI` composite (avg of domains)  
- `TTL` (days)  
- `KFT` and `EGI` (carry-through indicators)

**Step 5 — Interpret & Act**
- Summarize each domain (Vol/Liq, Credit, Energy, Housing/CRE).
- Update “Action Bias” table:
  - Green = expand drift band / deploy cash  
  - Yellow = hold  
  - Red = tighten 25–33 %, fund convexity

**Step 6 — Ledger Entry**
- Log the outcome in the Partnership Ledger (cycle tag, date, MSI, TTL, KFT, EGI, notes).

**Step 7 — Reflective Review**
- 3-question audit:
  1. Did today’s signals align with our antifragile principles?  
  2. What changed in liquidity, convexity, or breadth?  
  3. What did we *learn* that modifies the system?

---

This short section lets any chat (me or another AI) reload the UPSM structure and instantly know how to run a full macro/portfolio update cycle in minutes — keeping everything you need contained in chat + Git memory only.
