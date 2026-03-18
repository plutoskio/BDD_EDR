# Step 2 Foundation

This folder holds the canonical manual data foundation for Step 2 from [business_case_brief.md](/Users/milo/Desktop/BDD_EDR/business_case_brief.md).

It currently has two layers:

- a macro layer for normalized economic forecasts
- a positioning and themes layer for portfolio views and thematic calls
- a consolidated dashboard layer with one row per asset manager

## Files

- `macro_evidence.csv`
  - one row per manager and metric
  - this is the manual extraction sheet
  - fill `value`, `why`, `page`, and `raw_wording` here first
- `macro_master.csv`
  - one row per manager
  - this is the wide comparison table for analysis, dashboards, and downstream work
- `macro_codebook.md`
  - the rules for metric definitions and controlled numeric filling
- `positioning_evidence.csv`
  - raw source-backed extraction table for allocation, currencies, commodities, and themes
- `positioning_master.csv`
  - normalized comparison table with one row per manager and canonical topic
- `positioning_codebook.md`
  - the rules for topic coverage and view normalization
- `asset_manager_master.csv`
  - one row per asset manager
  - this is the simplest comparison table for dashboard work and manual review
  - it combines macro fields and qualitative topic fields in a single sheet
- `asset_manager_manual_entries.json`
  - sparse manual supplement for managers or fields that are not yet represented in `macro_master.csv` / `positioning_master.csv`
  - use this for newly added outlooks so rebuilds do not wipe them out

## Working Rule

Use the matching evidence table as the source of truth for each layer.

Recommended workflow:

1. Search the candidate source in `outlooks_txt/`.
2. Verify the final statement in the original file in `outlooks/`.
3. Fill the relevant row in `macro_evidence.csv` or append evidence to `positioning_evidence.csv`.
4. Mirror the final selected output into `macro_master.csv` or `positioning_master.csv`.
5. Add any net-new manager rows or manual overrides to `asset_manager_manual_entries.json`.
6. Rebuild `asset_manager_master.csv` with `python3 scripts/build_asset_manager_master.py`.
7. Use `asset_manager_master.csv` as the practical one-row-per-manager layer for dashboard building and manual comparison.

## Design Choices

- The macro layer keeps a numeric `value` column even when some values are proxied from qualitative wording.
- The positioning layer keeps a normalized `view` field rather than forcing fake numeric precision into allocation and theme calls.
- We intentionally do not keep `method` or `confidence` columns in the data tables.
- Rigor is preserved through:
  - `page`
  - `raw_wording`
  - a fixed codebook in `macro_codebook.md`
  - a fixed codebook in `positioning_codebook.md`

## Scope

The current macro foundation covers 12 metrics:

- `global_growth_2026`
- `us_gdp_2026`
- `eurozone_gdp_2026`
- `china_gdp_2026`
- `em_growth_2026`
- `global_inflation_2026`
- `us_inflation_2026`
- `eurozone_inflation_2026`
- `fed_year_end_rate_2026`
- `ecb_deposit_rate_year_end_2026`
- `snb_policy_rate_year_end_2026`
- `eur_usd_2026`

If the scope expands later, add new metrics to both `macro_evidence.csv` and `macro_master.csv` only after updating the codebook first.

## Positioning Scope

The current positioning and themes foundation covers five buckets:

- `equities`
- `fixed_income`
- `currencies`
- `commodities`
- `themes`

The canonical topic list lives in `positioning_codebook.md`.

`positioning_evidence.csv` starts as an empty audit log by design. Append raw statements there as they are found, then normalize them into the prefilled grid in `positioning_master.csv`.
