import json, os, time
from datetime import datetime, timezone

def fetch_or_placeholder():
    # TODO: pull your sources (Sheets CSV, APIs behind your keys in repo secrets, etc.)
    # return dict of latest metrics; here are safe placeholders
    return {
        "msi": {"composite": 2.85, "credit": 2.6, "energy": 3.1, "vol_liq": 2.9, "human_policy": 2.7, "fx_fragility": 2.8},
        "tripwires": {"vix_term_inversion": False, "hyg_lqd_premdisc_5d_abs": 0.18,
                      "wti_curve_state": "backwardation", "sofr_vs_corridor_bps": 3,
                      "rrp_balance_usd_b": 8.1, "srf_usage_usd_b": 3.2, "breadth_spxa50r": 52.0},
        "kft": 1.02, "egi": 18.5, "ttl_days": 26,
        "fx": {"dxy": 101.9, "real_10y": 1.65},
        "energy": {"wti_front": 78.4, "wti_z1_z6_bps": -85, "natgas_curve_state": "contango"},
        "credit": {"hy_oas_bps": 380, "ig_oas_bps": 110},
        "notes": "Auto-build placeholder."
    }

def main():
    data = fetch_or_placeholder()
    packet = {
        "asof": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "schema_version": "1.2",
        **data
    }
    os.makedirs("state", exist_ok=True)
    with open("state/context.json", "w") as f:
        json.dump(packet, f, indent=2)
    os.makedirs("history", exist_ok=True)
    with open(f"history/context_{int(time.time())}.json", "w") as f:
        json.dump(packet, f)

if __name__ == "__main__":
    main()
