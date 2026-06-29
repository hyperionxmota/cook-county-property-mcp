# Cook County / Chicago Property Data — MCP server

A hosted, **pay-per-call** [Model Context Protocol](https://modelcontextprotocol.io) (MCP) server for **Cook County, Illinois — including the City of Chicago** — property records: parcels, recorded sales & deed history, building permits, and property-tax assessment history, joined and normalized into one answer. Plus comparable sales (comps) and a lightweight automated valuation.

No signup, no API key — pay per call via the [x402](https://x402.org) protocol (USDC on Base or Solana).

## What this adds over raw open data

This returns **finished, joined answers** — not raw rows you have to query and stitch. The county open data (Socrata) can't give you:

- **Building permits linked to a PIN.** The Chicago permits feed has **no PIN field** — the permit→parcel link is *derived here* (exact address match + nearest-parcel geo match). You can't reproduce this with a raw SoQL query.
- **A street address on a parcel.** Parcel Universe has **no address**; it's joined in from a separate dataset here.
- **Comparable-sales valuation.** Arm's-length filtering, same-neighborhood/class matching, and an implied low/median/high range — derived analysis, not a row fetch.

So one call returns a normalized property record; against raw open data you'd orchestrate multiple datasets and rebuild joins that don't exist upstream.

## Connect

- **Remote MCP endpoint:** `https://api.ingest0r.com/mcp` (streamable-http — add it to any MCP client; nothing to install)
- **Smithery:** [`ingest0r/cook-county-property-data`](https://smithery.ai/server/ingest0r/cook-county-property-data)
- **Official MCP Registry:** `com.ingest0r.api/cook-county-property-data`
- **Website / HTTP API:** https://api.ingest0r.com
- **Free example response (no payment):** https://api.ingest0r.com/v1/sample

## Tools

| Tool | Price | Description |
|------|-------|-------------|
| `search_chicago_property_by_address` | $0.01 | Resolve a street address &rarr; parcel PIN(s). The no-PIN entry point. |
| `get_cook_county_parcel` | $0.01 | Single parcel record by 14-digit PIN. |
| `get_cook_county_property_dossier` | $0.03 | Full dossier: address, sales &amp; deed history, permits, assessment history. |
| `find_chicago_comparable_sales` | $0.10 | Comparable sales + implied low/median/high valuation. |

Data tools return an HTTP **402** with machine-readable x402 payment terms; pay in USDC and retry.

## Data & coverage

~1.9M parcels, refreshed nightly from Cook County Assessor, Cook County Recorder of Deeds, and City of Chicago open-data portals (Socrata). **Property-keyed public records only — no owner/occupant personal data.**

## Use cases

Real-estate due diligence, automated valuation / comps, title & lien research prep, lead enrichment, and market analysis — for autonomous agents and LLM pipelines.
