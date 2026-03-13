# Step 2 Foundation

This folder holds the canonical manual data foundation for Step 2 from [business_case_brief.md](/Users/milo/Desktop/BDD_EDR/business_case_brief.md).

The goal is to maximize quantitative coverage while keeping every filled value traceable to a page and raw wording in the source.

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

## Working Rule

Use `macro_evidence.csv` as the source of truth.

Recommended workflow:

1. Search the candidate source in `outlooks_txt/`.
2. Verify the final statement in the original file in `outlooks/`.
3. Fill the row in `macro_evidence.csv`.
4. Mirror the final selected value into `macro_master.csv`.

## Design Choices

- We intentionally keep a numeric `value` column even when some values are proxied from qualitative wording.
- We intentionally do not keep `method` or `confidence` columns in the data tables.
- Rigor is preserved through:
  - `page`
  - `raw_wording`
  - a fixed codebook in `macro_codebook.md`

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
