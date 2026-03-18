# Coding Consistency Review

This note is the rulebook for keeping `asset_manager_master.csv` comparable across managers.

## Why This Review Matters

The row-level audit answered: "does this row match its source?"

This consistency review answers: "are similar statements coded the same way across managers?"

Without this second step, the dataset can create false differences:

- one manager gets `positive` where another gets `overweight`
- one narrative macro statement gets `qualitative` while a similar one gets a fake numeric midpoint
- one selective credit view gets coded into a specific bucket while another stays only at the broad asset-class level

That would weaken any later interpretation of consensus, divergence, or EdRAM uniqueness.

## Current Structure

The master has two main coding layers:

- macro fields:
  - `*_status`
  - `*_value`
  - `*_why`
  - `*_page`
  - `*_raw_wording`
- qualitative fields:
  - `*_view`
  - `*_why`
  - `*_page`
  - `*_raw_wording`

## Canonical Rules

### 1. Macro Status

Use:

- `quantitative`
  - only when the outlook gives an explicit 2026 point estimate, explicit year-end rate, or clear numeric target/range that can be defensibly encoded
- `qualitative`
  - when the outlook gives a directional or approximate view but not a clean comparable point estimate
- `ND`
  - when the outlook does not provide a usable signal

Rule:

- if `*_status = qualitative`, then `*_value` must be blank
- if `*_status = ND`, then `*_value`, `*_why`, `*_page`, and `*_raw_wording` should be blank

Examples:

- `US growth slows materially` -> `qualitative`
- `Fed cuts another 75bp` -> usually `qualitative` unless a clear year-end level is stated or directly implied
- `EUR/USD at 1.20 by end-2026` -> `quantitative`

### 2. Geography / Asset Views

Use `view` labels as directional preference labels, not portfolio sizing jargon.

Preferred standard set:

- `positive`
- `neutral`
- `mixed`
- `negative`
- `ND`

Interpretation:

- `positive`
  - preferred, attractive, constructive, overweight-like, favored
- `neutral`
  - equal weight, balanced, fair, hold
- `mixed`
  - constructive with explicit caveats, split horizon, selective only, or internally conflicting message
- `negative`
  - unattractive, underweight-like, avoid, less preferred

Recommendation:

- normalize `overweight` -> `positive`
- normalize `underweight` -> `negative`

Those labels are currently mixed into:

- `equities_overall_view`
- `equities_geography_us_view`
- `equities_geography_em_view`
- `equities_geography_japan_view`
- `fixed_income_segment_government_bonds_view`

### 3. Duration

`fixed_income_duration_view` is a different axis from other `view` fields. It should describe direction on duration, not broad conviction.

Preferred standard set:

- `long`
- `neutral`
- `short`
- `ND`

Recommendation:

- convert duration entries currently coded as `positive` into `long` or `neutral` depending on wording

Current inconsistency:

- some rows use `long` / `short`
- others use `positive`

This makes the field semantically inconsistent.

### 4. Geopolitical Risk Theme

This field should represent whether geopolitics is treated mainly as:

- a downside risk -> `negative`
- both risk and opportunity / hedge rationale -> `mixed`
- `ND`

Recommendation:

- keep `mixed` only when the outlook explicitly frames geopolitics as both a risk and an investable opportunity
- otherwise default to `negative`

### 5. Broad vs Specific Coding

If the source only says something broad like:

- `constructive on bonds`

then code only the broad field:

- `fixed_income_overall_view = positive`

Do not automatically fill:

- `investment_grade`
- `government_bonds`
- `duration`

unless the wording explicitly supports those buckets.

Likewise:

- `constructive on Europe` does not automatically mean `small caps positive`
- `selective on credit` does not automatically mean `high yield positive`

### 6. Mixed Should Be Used Narrowly

Use `mixed` only when one of the following is true:

- the source is explicitly two-sided
- the manager is constructive but highly selective
- the horizon is split, for example near-term neutral but medium-term positive
- the field combines offsetting signals

Do not use `mixed` as a vague synonym for uncertainty.

## Concrete Issues Found

### Fixed

- `Lazard` had four macro fields correctly downgraded to `qualitative`, but the old numeric values were still present in the row. Those values have now been blanked in the manual layer.

### Still Worth Standardizing

1. `overweight` / `underweight` mixed with `positive` / `negative`

Current examples:

- `BlackRock` US equities = `overweight`
- `LGT Capital Partners` US equities = `underweight`
- `Generali AM` equities overall = `overweight`

Recommendation:

- convert those to directional labels for consistency:
  - `overweight` -> `positive`
  - `underweight` -> `negative`

2. `fixed_income_duration_view` mixes axis labels and conviction labels

Current examples:

- `JP Morgan AM` = `long`
- `EdRAM` = `short`
- `PGIM` = `positive`
- `AllianzGI` = `positive`

Recommendation:

- convert duration to only `long`, `neutral`, `short`

3. `themes_geopolitical_risk_view` uses both `negative` and `mixed`

Current `mixed` rows:

- `Amundi`
- `Goldman Sachs AM`
- `Santander AM`
- `UBS`

Recommendation:

- keep `mixed` only if the source clearly treats geopolitics as both a risk and an investable theme
- otherwise standardize to `negative`

## Proposed Minimal Standardization Pass

Before interpretation work begins, do one short cleanup pass:

1. Remove all `overweight` / `underweight` values from `*_view` fields and convert them to `positive` / `negative`.
2. Normalize `fixed_income_duration_view` to `long` / `neutral` / `short`.
3. Confirm that every `qualitative` macro field has a blank `value`.
4. Recheck `themes_geopolitical_risk_view` to ensure `mixed` is used only where explicitly justified.

## Recommended Interpretation Standard

After this pass, the dataset can be read as:

- macro:
  - `quantitative` = explicit numeric disclosure
  - `qualitative` = usable directional disclosure
  - `ND` = no usable disclosure
- qualitative views:
  - `positive`, `neutral`, `mixed`, `negative`, `ND`
- duration only:
  - `long`, `neutral`, `short`, `ND`

That is the cleanest structure for future comparison work.
