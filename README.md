# code_snippets/v1 — metric scripts by chapter

Built 2026-10-08 from `writing_plans/Code_Proposals_by_Chapter_2026-10-08.md`.
Folders use the **current** chapter numbers (Ch 1–12 + Appendix A).

## Use

```bash
pip install -r requirements.txt
python run_selftests.py                        # all 37 scripts, offline, synthetic data
python ch04_etp/ch04_ics.py --selftest         # one script
python ch10_moving_averages/ch10_crossover_backtest.py SPY   # live (yfinance)
```

Each script has the same shape:
- a module docstring whose **Ref:** line names the book paragraph or PROOF step it implements;
- pure `compute`-style functions;
- `--selftest`, which runs offline on synthetic data or on the book's own numbers;
- an optional live mode.

Network libraries are imported lazily, so `--selftest` never needs the internet.

SQL files are PostgreSQL. All 12 were executed on PostgreSQL 16 and every view was queried against sample data. Run them in folder order: Ch 9 reads views and tables from Ch 2, Ch 5 and Ch 7.

## Shared layer — `common/`

| File | Contents |
|---|---|
| `data.py` | `get_ohlcv` (yfinance / Kraken / CSV), `check_ohlcv`, `synthetic_ohlcv`, `get_fred` |
| `indicators.py` | Wilder, EMA, SMA, TR/ATR, RSI, MACD, ADX/DI, Bollinger, Stochastic + Williams %R, CCI, OBV, crosses |
| `stats.py` | forward returns, Sharpe, CAGR, max drawdown, Mann-Whitney edge, hit rate |
| `backtest.py` | minimal vectorised long/flat/short backtest with costs |

## Index

| Folder | Script | Book reference |
|---|---|---|
| `ch02_stocks` | `ch02_screen_scorecard.py` | §2.3–2.4, PROOF §2.9 (reproduces NVIDIA: avg NI $34.9B, 168× cycle P/E, $23 fair price, CFI 0.90) |
| | `ch02_cash_conversion_trend.py` | §2.3.3, PROOF §2.9.5 |
| | `ch02_fundamentals.sql` | §2.3, §2.4.1, Table 2.2 |
| `ch03_bonds_intermarket` | `ch03_bond_endpoints.py` | §3.12.1 (the missing `bond_data_endpoints.py`), PROOF §3.13.1 |
| | `ch03_bond_metrics.py` | §3.2.2, §3.2.4 (5.67% / 4.37%), PROOF §3.13.4 |
| | `ch03_bond_score.py` | §3.3–3.4 (Table 3.3 weights) |
| | `ch03_stock_bond_regime.py` | §3.10.2, §3.11 Rule A, PROOF §3.13.5 |
| | `ch03_macro_series.sql` | §3.12.2, §3.10, PROOF §3.13.1 |
| `ch04_etp` | `ch04_ics.py` | §4.4, PROOF §4.8 (reproduces Tables 4.3, 4.5, 4.8, 4.9) |
| | `ch04_spread_sampler.py` | §4.4.5, PROOF §4.8.2 |
| | `ch04_tracking_difference.py` | §4.4.6, PROOF §4.8.6 |
| | `ch04_etp_catalog.sql` | §4.1.2, §4.4.5, §4.4.8 |
| `ch05_futures` | `ch05_curve_roll.py` | §5.2.2–5.2.3, Ch 6 PROOF §6.4.1–6.4.3 |
| | `ch05_margin_monitor.py` | §5.3, §5.5.1, PROOF §5.9.2 (reproduces Table 5.8) |
| | `ch05_front_month.py` | §5.1.5, §5.6.5 |
| | `ch05_futures.sql` | §5.1.5, §5.2.3, §5.6.5 |
| `ch06_etc_etn` | `ch06_etc_vs_futures_gap.py` | §6.1.3, §6.1.5, PROOF §6.4.7 |
| | `ch06_carry_trend_screen.py` | §6.1.4, §6.1.6, PROOF §6.4.4–6.4.8 |
| | `ch06_cot_positioning.py` | PROOF §6.4.6; Ch 9 §9.7.3 mapping |
| | `ch06_crypto_etn_premium.py` | §6.2.8–6.2.9 |
| | `ch06_cot.sql` | PROOF §6.4.6, §6.2.9 |
| `ch07_options` | `ch07_payoff_and_greeks.py` | §7.4–7.6, PROOF §7.9 (adds Vega, payoff diagram) |
| | `ch07_iv_metrics.py` | §7.4.2, PROOF §7.9.1 |
| | `ch07_option_chain.sql` | §7.5, §7.8, PROOF §7.9.1 |
| `ch08_ta_foundations` | `ch08_ohlcv_quality.py` | §8.10 Hands-On, §8.5.2 |
| | `ch08_trend_structure.py` | §8.7–8.9, PROOF §8.10 |
| | `ch08_random_walk_tests.py` | §8.4.2, §8.1.2 |
| | `ch08_ohlcv.sql` | §8.10, §8.9.2 |
| `ch09_volume_oi` | `ch09_volume_signal_board.py` | §9.3.1, §9.4.2, §9.9.3, PROOF §9.11 |
| | `ch09_price_oi_matrix.py` | §9.2, §9.5, §9.6, PROOF §9.11 |
| | `ch09_volume_edge_test.py` | §9.3.2, PROOF §9.11 |
| | `ch09_put_call_ratio.py` | §9.8, PROOF §9.11 |
| | `ch09_volume_oi.sql` | Listings 9.2/9.4, §9.5, §9.8, §9.9.3 |
| `ch10_moving_averages` | `ch10_ma_state.py` | §10.3–10.5, §10.9.3 |
| | `ch10_crossover_backtest.py` | §10.2, §10.4, PROOF §10.11 |
| | `ch10_walkforward_ma.py` | §10.8.1, PROOF §10.11 check 3 |
| | `ch10_ma.sql` | §10.4.1, §10.10, PROOF §10.11 |
| `ch11_oscillators` | `ch11_oscillator_panel.py` | §11.1–11.6, §11.10, §11.9.3 |
| | `ch11_mtf_rsi_stack.py` | §11.7.2 DATA box (the promised 3-layer stack; look-ahead tested) |
| | `ch11_sentiment_extremes.py` | §11.8 |
| | `ch11_oscillators.sql` | Listing 11.5, PROOF §11.11 |
| `ch12_adx` | `ch12_regime_gate.py` | §12.4, §12.7, §12.10.3, §12.9.3 |
| | `ch12_cross_market_adx.py` | §12.7.3 |
| | `ch12_adx_filter_value.py` | PROOF §12.11 (non-overlapping returns) |
| | `ch12_regime.sql` | §12.4.2, §12.7.3, §12.9.4 |
| `appendix_a` | `appx_a_portfolio_limits.py` | §A.2, §A.2.2, §A.3.1, PROOF §A.13 checks 1–4 |
| | `appx_a_trade_journal_metrics.py` | §A.3.3, §A.9.2, §A.10, PROOF §A.13 checks 5–8 |
| | `appx_a_risk_of_ruin.py` | §A.2.2, Ch 5 §5.5.2 |
| | `appx_a_journal.sql` | §A.9.2, §A.2, PROOF §A.13 |

## Listing size (for excerpts in the book)

Code is formatted to 88 characters. Excerpt one function per listing, aim for 10–20 lines, and cite the full file with a "Full version: `code_snippets/v1/…`" line (proposal doc §0.1).
