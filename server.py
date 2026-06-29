"""Cook County / Chicago Property Data — MCP server (stdio).

A thin Model Context Protocol proxy over the hosted HTTP API at
https://api.ingest0r.com. It exposes four read tools; each is pay-per-call via the
x402 protocol (USDC on Base or Solana). When payment is required the underlying API
returns HTTP 402, which this server surfaces verbatim so an x402-capable client can
pay and retry. No API key or signup.

Run:  python server.py            (stdio transport)
Env:  API_BASE_URL                (default https://api.ingest0r.com)
"""

from __future__ import annotations

import os
from typing import Annotated
from urllib.parse import quote

import httpx
from pydantic import Field
from mcp.server.fastmcp import FastMCP

API = os.environ.get("API_BASE_URL", "https://api.ingest0r.com").rstrip("/")

mcp = FastMCP(
    "cook-county-chicago-property-data",
    instructions=(
        "Cook County / Chicago property records via a hosted, pay-per-call API. "
        "Resolve a street address to a parcel PIN with "
        "search_chicago_property_by_address, then call "
        "get_cook_county_property_dossier (full record), get_cook_county_parcel "
        "(cheap single lookup), or find_chicago_comparable_sales (comps + "
        "valuation). These data tools return joined, derived answers — including permit→PIN links and comparable-sales valuation that raw Cook County open-data / SoQL queries can't return, not raw rows to stitch. Each is paid per call via x402 (USDC on Base or "
        "Solana) and returns an HTTP 402 with machine-readable payment terms until "
        "paid. Coverage: Cook County, Illinois incl. the City of Chicago; public "
        "records only, no personal data."
    ),
)

_PIN = Annotated[str, Field(description=(
    "14-digit Cook County PIN, digits or dashed form (e.g. '14081200170000' or "
    "'14-08-120-017-0000'); a 10-digit PIN is also accepted. Use "
    "search_chicago_property_by_address first if you only have a street address."))]


def _get(path: str) -> dict:
    r = httpx.get(f"{API}{path}", timeout=30)
    if r.status_code == 402:
        return {"error": "payment_required", "x402": r.json()}
    if r.status_code == 429:
        return {"error": "rate_limited"}
    r.raise_for_status()
    return r.json()


def _seg(prefix: str, arg: str) -> str:
    return f"{prefix}/{quote(str(arg), safe='')}"


@mcp.tool()
def search_chicago_property_by_address(
    address: Annotated[str, Field(description=(
        "Full or partial Cook County / Chicago street address, at least ~4 "
        "characters, e.g. '1 E 113th St' or '5352 N Magnolia Ave'."))],
) -> dict:
    """Resolve a Cook County / Chicago street address to its parcel PIN(s).

    The no-PIN entry point: when you have a street address but not a 14-digit PIN,
    call this FIRST, then pass a returned `pin` to get_cook_county_parcel,
    get_cook_county_property_dossier, or find_chicago_comparable_sales. Returns
    ranked candidate parcels, each with `pin`, `prop_address`, `prop_city`,
    `prop_zip`, and a 0-1 `score` (address similarity). Source: Cook County
    Assessor address records. Paid: $0.01 per call via x402.
    """
    return _get(_seg("/v1/search", address))


@mcp.tool()
def get_cook_county_parcel(pin: _PIN) -> dict:
    """Look up a single Cook County / Chicago parcel by PIN.

    Returns the parcel record: street address, city, ZIP, assessor property class,
    township, neighborhood code, ward/municipality, latitude/longitude, and tax
    year. The cheap single-property lookup; use get_cook_county_property_dossier
    when you also need sales, permits, and assessment history. Paid: $0.01 per
    call via x402. Source: Cook County Assessor, refreshed nightly.
    """
    return _get(_seg("/v1/parcel", pin))


@mcp.tool()
def get_cook_county_property_dossier(pin: _PIN) -> dict:
    """Full property dossier for a Cook County / Chicago parcel in one call.

    Returns parcel basics PLUS recorded sales & deed history, building permits,
    and property-tax assessment history, joined and normalized into one record —
    the one-call due-diligence answer. Permits are LINKED to the PIN here (the raw permit open-data has no PIN; links are derived by address + geo match) — a join you can't reproduce with raw open-data queries. Use for valuation, underwriting, title and
    lien research prep, and lead enrichment. Paid: $0.03 per call via x402. Public
    records only; no owner or occupant personal data.
    """
    return _get(_seg("/v1/dossier", pin))


@mcp.tool()
def find_chicago_comparable_sales(pin: _PIN) -> dict:
    """Comparable sales (comps) and a lightweight valuation for a Cook County / Chicago property.

    Returns recent arm's-length sales in the same assessor neighborhood and
    property class as the subject PIN (last ~18 months), plus an implied
    low/median/high price range. Non-arm's-length and multi-parcel deeds are
    filtered out — a derived valuation you won't get from a raw open-data query. Use for valuation, investment screening, and underwriting.
    Paid: $0.10 per call via x402.
    """
    return _get(_seg("/v1/comps", pin))


if __name__ == "__main__":
    mcp.run()
