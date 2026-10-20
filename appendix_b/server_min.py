"""server_min.py -- Appendix B: a read-only decision-support MCP server.

Ref: §B.4 Listings B.1 (market_regime) and B.2 (position_gate), §B.5 PROOF.
Regime thresholds from Chapter 12 (ADX > 25 trend, < 20 stand aside);
position gate from Appendix A (2% risk per trade, 3:1 reward-to-risk floor).
The server never exposes an order function (§B.2.1, exposure ladder).

Usage:
    python appendix_b/server_min.py --selftest   # offline, synthetic data
    python appendix_b/server_min.py              # stdio server for Claude/Cursor
    npx @modelcontextprotocol/inspector python3 appendix_b/server_min.py

Needs:  pip install "mcp>=2.0"   (the selftest runs without it)
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # code_snippets/v1

from common.data import get_ohlcv  # noqa: E402
from common.indicators import adx, rsi  # noqa: E402

try:
    from mcp.server.mcpserver import MCPServer
except ImportError:  # SDK not installed: --selftest still runs

    class MCPServer:  # minimal stand-in, same decorator shape
        def __init__(self, name: str, instructions: str = "") -> None:
            self.name = name

        def tool(self):
            return lambda fn: fn

        def run(self) -> None:
            sys.exit('MCP SDK missing: pip install "mcp>=2.0"')


mcp = MCPServer("pft-decision-support", instructions=
    "Read-only tools. Date every number. Never recommend an order.")

# ---------------------------------------------------------------- Listing B.1
@mcp.tool()
def market_regime(pair: str = "XBTUSD") -> dict:
    """Daily ADX regime + RSI(14), last CLOSED bar.
    ADX > 25 trend, < 20 stand aside (Chapter 12)."""
    df = get_ohlcv(pair, "1d", source="kraken")
    d, i = adx(df), -2                  # -1 is still forming
    a = float(d["adx"].iloc[i])
    return {"date": str(df.index[i].date()), "adx": round(a, 1),
            "plus_di": round(float(d["plus_di"].iloc[i]), 1),
            "minus_di": round(float(d["minus_di"].iloc[i]), 1),
            "rsi": round(float(rsi(df["close"]).iloc[i]), 1),
            "regime": "trend" if a > 25 else
                      "stand aside" if a < 20 else "transition"}


# ---------------------------------------------------------------- Listing B.2
@mcp.tool()
def position_gate(equity: float, entry: float,
                  stop: float, target: float) -> dict:
    """2% risk size and reward-to-risk (Appendix A).
    Returns a verdict; never places an order."""
    unit = abs(entry - stop)
    if unit == 0:
        return {"verdict": "REJECT: stop equals entry"}
    rr = abs(target - entry) / unit
    return {"max_size": round(0.02 * equity / unit, 4),
            "risk_at_max": round(0.02 * equity, 2),
            "reward_risk": round(rr, 2),
            "verdict": "OK" if rr >= 3 else "SKIP: below 3:1"}


# ---------------------------------------------------------------- selftest
def selftest() -> None:
    r = market_regime("SYNTH")  # get_ohlcv returns synthetic bars for SYNTH
    assert set(r) == {"date", "adx", "plus_di", "minus_di", "rsi", "regime"}, r
    want = "trend" if r["adx"] > 25 else "stand aside" if r["adx"] < 20 else "transition"
    assert r["regime"] == want and 0 <= r["rsi"] <= 100, r
    # §B.5.1 worked check: EUR 25,000, stop 4% below entry, target 12% above
    g = position_gate(25_000, 100, 96, 112)
    assert g == {"max_size": 125.0, "risk_at_max": 500.0, "reward_risk": 3.0, "verdict": "OK"}, g
    assert g["max_size"] * 100 == 12_500  # notional at the 2% limit
    assert position_gate(25_000, 100, 96, 108)["verdict"].startswith("SKIP")
    assert position_gate(25_000, 100, 100, 110)["verdict"].startswith("REJECT")
    print(f"market_regime(SYNTH) -> {r}")
    print(f"position_gate(25000, 100, 96, 112) -> {g}")
    print("selftest OK")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    else:
        mcp.run()  # stdio: the host starts this process
