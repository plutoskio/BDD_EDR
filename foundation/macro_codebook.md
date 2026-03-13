# Macro Codebook

This codebook is designed to increase quantitative coverage without turning the dataset into uncontrolled guesswork.

Every filled value must have:

- `page`
- `raw_wording`
- `why`

## Fill Order

For each manager and each metric, use the first rule below that applies:

1. Published point estimate
2. Published range midpoint
3. Derived point from an explicit path
4. Controlled qualitative proxy
5. `ND` if the source is too vague

Do not leave the raw wording blank when a value is filled.

## Required Fields

- `value`
  - the final numeric value used in comparison work
- `why`
  - short driver summary in plain English
  - keep it short, ideally one clause
- `page`
  - page number like `12`, `12-13`, or `docx-unpaginated`
- `raw_wording`
  - the key sentence or short passage that justifies the value

## Metric Definitions

- `global_growth_2026`
  - world or global GDP growth for 2026
- `us_gdp_2026`
  - U.S. GDP growth for 2026
- `eurozone_gdp_2026`
  - Eurozone GDP growth for 2026
- `china_gdp_2026`
  - China GDP growth for 2026
- `em_growth_2026`
  - emerging markets growth for 2026
- `global_inflation_2026`
  - world or global inflation for 2026
- `us_inflation_2026`
  - U.S. inflation for 2026
- `eurozone_inflation_2026`
  - Eurozone inflation for 2026
- `fed_year_end_rate_2026`
  - Fed policy rate or closest stated year-end 2026 policy target
- `ecb_deposit_rate_year_end_2026`
  - ECB deposit rate or closest stated year-end 2026 policy target
- `snb_policy_rate_year_end_2026`
  - SNB policy rate or closest stated year-end 2026 policy target
- `eur_usd_2026`
  - year-end 2026 EUR/USD target or closest explicit 2026 target

## Quantitative Rules

### 1. Published Point Estimate

If the source gives a clean number, keep it.

Examples:

- `U.S. growth 1.5%`
- `Fed funds at 3.25-3.50% by year-end` if a single midpoint is not required by the source
- `EUR/USD at 1.20`

For policy-rate corridors:

- convert to midpoint for `value`
- keep the full corridor in `raw_wording`

Example:

- `3.25-3.50%` becomes `3.375`

### 1a. Anchored Verbal Number

If the source anchors the statement to a number but uses soft qualifiers, convert it to
the nearest simple numeric point and keep the wording in `raw_wording`.

Allowed examples:

- `around 4.5%` becomes `4.5`
- `slightly above 1%` becomes `1.1`
- `a little more than 4%` becomes `4.1`
- `above 3%` becomes `3.1`
- `below 2%` becomes `1.9`
- `around potential` should not use this rule unless the potential level is stated

Use this rule only when the statement still contains an explicit numeric anchor.

### 2. Published Range Midpoint

If the source gives a range, use the midpoint.

Examples:

- `1.2-1.5%` becomes `1.35`
- `1.16-1.19` becomes `1.175`

### 3. Derived Point From An Explicit Path

Use this only when the path is explicit enough to compute a number directly.

Allowed examples:

- `one more 25bp ECB cut` from a clearly known starting rate
- `two Fed cuts from the current range`
- `SNB remains at 0%`

If the starting point is not explicit in the source or not obvious from the document context, do not derive the number.

### 4. Controlled Qualitative Proxy

Use this only when there is no point or range, but the wording is directional enough to support a numeric proxy.

The proxy must be based on the median explicit value already observed in the corpus for that metric, then adjusted by a fixed delta.

#### Growth And Inflation Delta Grid

Apply these deltas around the corpus median explicit value for the same metric:

- `sharp slowdown`, `recessionary`, `contracts`, `below trend`: `-0.50`
- `slowing`, `soft`, `modest`, `weaker`: `-0.25`
- `stable`, `resilient`, `around trend`, `steady`: `0.00`
- `improving`, `pickup`, `moderate rebound`: `+0.25`
- `reaccelerates`, `strong rebound`, `above trend`: `+0.50`

#### Policy Rate Proxy Rules

Prefer explicit cut or hold language over generic tone.

Allowed rules:

- `on hold` = current policy rate carried to year-end 2026
- `one cut` = current rate minus `0.25`
- `two cuts` = current rate minus `0.50`
- `one hike` = current rate plus `0.25`

Do not proxy rates from vague language like `more accommodative` unless the same passage also gives a clear cut count or terminal direction.

#### EUR/USD Proxy Grid

Apply these deltas around the corpus median explicit `eur_usd_2026` value:

- `stable dollar`, `range-bound`: `0.00`
- `slightly weaker dollar`: `+0.03`
- `weaker dollar`: `+0.05`
- `materially weaker dollar`: `+0.08`
- `slightly stronger dollar`: `-0.03`
- `stronger dollar`: `-0.05`
- `materially stronger dollar`: `-0.08`

## When To Use `ND`

Use `ND` when:

- the source gives no usable statement for the metric
- the wording is too vague to justify a controlled proxy
- the statement is about a different horizon
- the statement is not specific enough to distinguish the metric

## Horizon Rules

Use the closest available 2026 reference in this order:

1. Full-year 2026 estimate
2. Year-end 2026 target
3. Latest explicit 2026 point in the source

If the source only gives a 2027 endpoint for a policy rate but clearly frames it as the continuation of the 2026 path, record it only if that is the closest explicit policy endpoint available and note that limitation in `raw_wording`.

## Writing Rules For `why`

The `why` field should summarize the driver, not repeat the full quote.

Good examples:

- `German fiscal support lifts Europe`
- `Sticky inflation delays Fed easing`
- `AI capex and fiscal stimulus support U.S. growth`
- `Dollar weakness supports EM and gold`

Avoid long sentences, quotations, and multiple unrelated drivers.
