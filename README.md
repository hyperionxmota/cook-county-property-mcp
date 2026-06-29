# Cook County / Chicago Property Data — MCP server

A hosted, **pay-per-call** [Model Context Protocol](https://modelcontextprotocol.io) (MCP) server for **Cook County, Illinois — including the City of Chicago** — property records: parcels, recorded sales & deed history, building permits, and property-tax assessment history, joined and normalized into one answer. Plus comparable sales (comps) and a lightweight automated valuation.

No signup, no API key — pay per call via the [x402](https://x402.org) protocol (USDC on Base or Solana).

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
