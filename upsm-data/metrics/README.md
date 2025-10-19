# UPSM /metrics (expanded minimal)

- **BTC_USD_DAILY** (canonical: CoinGecko) — sharded by year
- **IBIT_DAILY_FLOWS** — sharded by year
- **IBIT_USD_DAILY_CLOSE** — sharded by year
- **CME_BTC_FRONT_SETTLE** — sharded by year
- **PERP_FUNDING_8H** (Binance/Bybit/OKX) — sharded by month

**Conventions**
- JSON Lines (`.jsonl`), append-only
- UTC dates `YYYY-MM-DD`
- `source_lock.json` specifies canonical + fallbacks
- Do calculations live; persist only raw data or heavy/expensive outputs
