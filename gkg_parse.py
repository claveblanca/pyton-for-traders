"""
gkg_parse.py — load a GDELT GKG 2.1 file (no header) and label its fields, incl. GCAM.

Target news categories (from V2Themes): economy, trading, crypto, geopolitics, commodities.

Usage:
    python gkg_parse.py path/to/20261030143000.gkg.csv
"""
from __future__ import annotations

import sys
from typing import Literal

import pandas as pd

Category = Literal["economy", "trading", "crypto", "geopolitics", "commodities"]
CATEGORIES: tuple[Category, ...] = (
    "economy",
    "trading",
    "crypto",
    "geopolitics",
    "commodities",
)
# First match wins for primary_category when several apply
_CATEGORY_PRIORITY: tuple[Category, ...] = (
    "geopolitics",
    "crypto",
    "commodities",
    "trading",
    "economy",
)

# ECON_* themes treated as markets / FX / trade (rest of ECON_* -> economy)
_TRADING_ECON = frozenset(
    {
        "ECON_STOCKMARKET",
        "ECON_IPO",
        "ECON_CURRENCY_EXCHANGE_RATE",
        "ECON_WORLDCURRENCIES",
        "ECON_FREETRADE",
        "ECON_TRADE_DISPUTE",
        "ECON_EARNINGSREPORT",
        "ECON_BUBBLE",
        "ECON_FOREIGNINVEST",
    }
)

_COMMODITY_THEMES = frozenset(
    {
        "AGRICULTURE",
        "FOOD_STAPLE",
        "FOOD_SECURITY",
        "FUELPRICES",
        "ECON_OILPRICE",
        "ECON_GASOLINEPRICE",
        "ECON_GOLDPRICE",
        "ECON_NATGASPRICE",
        "ECON_DIESELPRICE",
        "ECON_HEATINGOILPRICE",
        "ECON_PROPANEPRICE",
        "ECON_ELECTRICALPRICE",
    }
)

_COMMODITY_PREFIXES = (
    "ENV_OIL",
    "ENV_NATURALGAS",
    "ENV_COAL",
    "ENV_METALS",
    "ENV_MINING",
    "ENV_GAS",
    "ENV_FISHERY",
    "ENV_FORESTRY",
)

_CRYPTO_KEYWORDS = ("BITCOIN", "CRYPTO", "BLOCKCHAIN", "ETHER", "DEFI", "NFT")

_GEO_SUBSTRINGS = (
    "ARMEDCONFLICT",
    "MILITARY",
    "SANCTION",
    "CONFLICT",
    "VIOLENCE",
    "TERROR",
    "REBELLION",
    "INSURGENCY",
    "WAR_",
    "ELECTION",
    "IMPEACHMENT",
    "REFUGEE",
    "BORDER",
    "CYBER_ATTACK",
    "HOSTAGE",
    "ASSASSINATION",
    "EXTREMISM",
    "JIHAD",
    "PIRACY",
    "KIDNAP",
    "POLITICS",
    "FRAGILITY_CONFLICT",
    "PEACEKEEPING",
    "NEGOTIATIONS",
    "BLOCKADE",
    "CEASEFIRE",
)

# --- 1. GKG 2.1 column names (27 columns, tab-separated, no header) -----------------
GKG_COLUMNS = [
    "GKGRECORDID", "DATE", "SourceCollectionIdentifier", "SourceCommonName",
    "DocumentIdentifier", "Counts", "V2Counts", "Themes", "V2Themes",
    "Locations", "V2Locations", "Persons", "V2Persons", "Organizations",
    "V2Organizations", "V2Tone", "Dates", "GCAM", "SharingImage", "RelatedImages",
    "SocialImageEmbeds", "SocialVideoEmbeds", "Quotations", "AllNames", "Amounts",
    "TranslationInfo", "Extras",
]

# V2Tone is 7 comma-separated numbers
TONE_FIELDS = ["tone", "positive", "negative", "polarity",
               "activity_density", "self_group_density", "word_count"]

GCAM_CODEBOOK_URL = "http://data.gdeltproject.org/documentation/GCAM-MASTER-CODEBOOK.TXT"


def load_gkg(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, sep="\t", header=None, names=GKG_COLUMNS, dtype=str,
                     quoting=3, encoding="utf-8", encoding_errors="replace")
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y%m%d%H%M%S", utc=True)
    tone = df["V2Tone"].str.split(",", expand=True).iloc[:, :7].astype(float)
    tone.columns = TONE_FIELDS
    return pd.concat([df, tone], axis=1)


def themes(s: str) -> list[str]:
    """V2Themes: 'THEME,charoffset;THEME,charoffset;...' -> unique theme names"""
    if not isinstance(s, str) or not s:
        return []
    return sorted({t.split(",")[0] for t in s.split(";") if t})


def categorize_theme(theme: str) -> set[Category]:
    """Map one GDELT theme string to zero or more target categories."""
    t = theme.upper()
    out: set[Category] = set()

    if t == "ECON_BITCOIN" or any(k in t for k in _CRYPTO_KEYWORDS):
        out.add("crypto")

    if t.startswith("ECON_") and t != "ECON_BITCOIN":
        out.add("trading" if t in _TRADING_ECON else "economy")

    if t.startswith("EPU_") and "ECON" in t:
        out.add("economy")
    if t.startswith("TAX_ECON") or t == "TAX_ECON_PRICE":
        out.add("economy")

    if t in _COMMODITY_THEMES or t.startswith(_COMMODITY_PREFIXES):
        out.add("commodities")

    if any(s in t for s in _GEO_SUBSTRINGS):
        out.add("geopolitics")
    if t.startswith(("MIL_", "GOV_", "POL_", "GENERAL_GOVERNMENT", "PROTEST")):
        out.add("geopolitics")
    if t.startswith("USPEC_POLITICS"):
        out.add("geopolitics")
    if t.startswith("USPEC_POLICY"):
        out.add("economy")

    return out


def categorize_themes(theme_list: list[str]) -> set[Category]:
    cats: set[Category] = set()
    for theme in theme_list:
        cats |= categorize_theme(theme)
    return cats


def primary_category(cats: set[Category]) -> str:
    for cat in _CATEGORY_PRIORITY:
        if cat in cats:
            return cat
    return ""


def apply_categories(df: pd.DataFrame) -> pd.DataFrame:
    """Add theme_list, categories, primary_category from V2Themes."""
    out = df.copy()
    out["theme_list"] = out["V2Themes"].map(themes)
    out["categories"] = out["theme_list"].map(
        lambda ts: sorted(categorize_themes(ts), key=CATEGORIES.index)
    )
    out["primary_category"] = out["categories"].map(
        lambda cs: primary_category(set(cs)) if cs else ""
    )
    return out


# --- 2. GCAM ---------------------------------------------------------------------
def parse_gcam(s: str) -> dict:
    """'wc:620,c1.2:3,c12.1:22,v10.1:5.41' -> {'wc': 620, 'c1.2': 3.0, ...}"""
    out = {}
    if not isinstance(s, str):
        return out
    for kv in s.split(","):
        k, _, v = kv.partition(":")
        if v:
            out[k] = float(v)
    return out


def load_codebook(path_or_url: str = GCAM_CODEBOOK_URL) -> pd.DataFrame:
    # columns: Variable, DictionaryID, DimensionID, Type, LanguageCode,
    #          DictionaryHumanName, DimensionHumanName, DictionaryCitation
    return pd.read_csv(path_or_url, sep="\t", dtype=str, encoding="latin-1")


def gcam_long(df: pd.DataFrame, codebook: pd.DataFrame) -> pd.DataFrame:
    """One row per (article, GCAM variable), labelled and normalised by word count."""
    rows = []
    for rid, g in zip(df["GKGRECORDID"], df["GCAM"]):
        d = parse_gcam(g)
        wc = d.pop("wc", None)
        for var, val in d.items():
            rows.append((rid, var, val, wc))
    long = pd.DataFrame(rows, columns=["GKGRECORDID", "Variable", "value", "wc"])
    long = long.merge(codebook, on="Variable", how="left")
    # c* = WORDCOUNT (words matching the dimension) -> normalise to share of article
    # v* = SCOREDVALUE (already an average score)  -> keep as is
    is_count = long["Variable"].str.startswith("c")
    long["score"] = long["value"]
    long.loc[is_count, "score"] = long.loc[is_count, "value"] / long.loc[is_count, "wc"]
    return long


if __name__ == "__main__":
    df = apply_categories(load_gkg(sys.argv[1]))
    print(df[["DATE", "SourceCommonName", "primary_category", "tone", "word_count"]].head(), "\n")
    print("Articles by primary category:\n", df["primary_category"].value_counts(), "\n")
    tagged = df[df["primary_category"] != ""]
    print(
        "Category coverage:",
        f"{len(tagged)}/{len(df)} articles with a category",
        f"({100 * len(tagged) / max(len(df), 1):.1f}%)\n",
    )
    print("Top themes:\n", df["theme_list"].explode().value_counts().head(15), "\n")

    cb = load_codebook()          # or a local copy of the codebook file
    long = gcam_long(df, cb)
    top = (long.groupby(["DictionaryHumanName", "DimensionHumanName"])["score"]
               .mean().sort_values(ascending=False).head(20))
    print("Strongest GCAM dimensions in this file:\n", top)
