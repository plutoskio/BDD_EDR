# Positioning And Themes Codebook

This codebook governs the Step 2 qualitative foundation for:

- asset class positioning
- currency and commodity views
- investment themes

It is the companion to `macro_codebook.md`, not a replacement for it.

## Goal

Capture how each manager wants to position a portfolio given its macro view.

This layer should answer questions such as:

- which equity markets are preferred or avoided
- whether large caps or small caps are favored
- whether investment grade or high yield is preferred
- whether duration should be short, neutral, or long
- whether the dollar, gold, or oil are supported
- which themes are investable, risky, or central to the house view

## Files

- `positioning_evidence.csv`
  - raw source-backed extraction table
  - one row per source statement
- `positioning_master.csv`
  - normalized comparison table
  - one row per manager and canonical topic

Use `positioning_evidence.csv` to collect raw statements first, then normalize into `positioning_master.csv`.

## Source Retrieval

Search `outlooks_txt/` first, then verify in `outlooks/`.

Useful search terms:

- equities: `equities`, `stocks`, `small caps`, `large caps`, `value`, `growth`, `quality`, `Europe`, `U.S.`, `EM`, `China`
- fixed income: `duration`, `credit`, `investment grade`, `high yield`, `sovereign`, `government bonds`, `corporate`, `EM debt`, `linkers`
- currencies: `dollar`, `USD`, `EUR`, `yen`, `JPY`, `FX`, `currency`
- commodities: `gold`, `oil`, `commodity`, `metals`
- themes: `AI`, `healthcare`, `energy transition`, `defense`, `sovereignty`, `geopolitics`, `infrastructure`, `resilience`

Typical sections in the source decks:

- `asset allocation`
- `equities`
- `fixed income`
- `FX`
- `commodities`
- `themes`
- `key ideas`
- `top convictions`

## Canonical Topic Grid

The normalized table uses the following `topic_id` values.

| topic_id | bucket | category | subcategory |
| --- | --- | --- | --- |
| `equities_overall` | `equities` | `overall` | `overall` |
| `equities_geography_us` | `equities` | `geography` | `us` |
| `equities_geography_europe` | `equities` | `geography` | `europe` |
| `equities_geography_japan` | `equities` | `geography` | `japan` |
| `equities_geography_em` | `equities` | `geography` | `em` |
| `equities_geography_china` | `equities` | `geography` | `china` |
| `equities_size_large_cap` | `equities` | `size` | `large_cap` |
| `equities_size_small_cap` | `equities` | `size` | `small_cap` |
| `equities_style_growth` | `equities` | `style` | `growth` |
| `equities_style_value` | `equities` | `style` | `value` |
| `equities_style_quality` | `equities` | `style` | `quality` |
| `fixed_income_overall` | `fixed_income` | `overall` | `overall` |
| `fixed_income_credit_quality_investment_grade` | `fixed_income` | `credit_quality` | `investment_grade` |
| `fixed_income_credit_quality_high_yield` | `fixed_income` | `credit_quality` | `high_yield` |
| `fixed_income_duration` | `fixed_income` | `duration` | `overall` |
| `fixed_income_segment_government_bonds` | `fixed_income` | `segment` | `government_bonds` |
| `fixed_income_segment_corporate_bonds` | `fixed_income` | `segment` | `corporate_bonds` |
| `fixed_income_segment_em_debt` | `fixed_income` | `segment` | `em_debt` |
| `fixed_income_segment_inflation_linked` | `fixed_income` | `segment` | `inflation_linked` |
| `currencies_overall` | `currencies` | `overall` | `overall` |
| `currencies_usd` | `currencies` | `currency` | `usd` |
| `currencies_eur` | `currencies` | `currency` | `eur` |
| `currencies_jpy` | `currencies` | `currency` | `jpy` |
| `currencies_em_fx` | `currencies` | `currency` | `em_fx` |
| `commodities_overall` | `commodities` | `overall` | `overall` |
| `commodities_gold` | `commodities` | `commodity` | `gold` |
| `commodities_oil` | `commodities` | `commodity` | `oil` |
| `commodities_industrial_metals` | `commodities` | `commodity` | `industrial_metals` |
| `themes_ai` | `themes` | `theme` | `ai` |
| `themes_healthcare` | `themes` | `theme` | `healthcare` |
| `themes_energy_transition` | `themes` | `theme` | `energy_transition` |
| `themes_geopolitical_risk` | `themes` | `theme` | `geopolitical_risk` |
| `themes_defense_sovereignty` | `themes` | `theme` | `defense_sovereignty` |
| `themes_other` | `themes` | `theme` | `other` |

## Allowed Views

The normalized `view` field is intentionally flexible.

For most topics, use:

- `overweight`
- `positive`
- `neutral`
- `negative`
- `underweight`
- `mixed`
- `ND`

For `fixed_income_duration`, use:

- `short`
- `neutral`
- `long`
- `barbell`
- `mixed`
- `ND`

## Coding Rules

1. Keep one normalized row per manager and `topic_id` in `positioning_master.csv`.
2. Put the final normalized interpretation in `view`.
3. Keep the supporting source sentence in `raw_wording`.
4. Use `why` for a short driver summary, not for a second quote.
5. If one source sentence supports multiple topics, duplicate the page and wording across the relevant rows.
6. If a source is too vague to support a topic, leave the master row blank until review is complete, then use `ND`.
7. Do not invent a positive or negative view when the text only says the asset class is important to monitor.

## Normalization Guidance

- `overweight` / `underweight`
  - use when the source clearly expresses portfolio allocation language
- `positive` / `negative`
  - use when the source gives a directional preference without explicit portfolio-weight wording
- `neutral`
  - use when the source is balanced, stable, or explicitly neutral
- `mixed`
  - use when the outlook is split, barbelled, or supportive but with strong stated offsets
- `ND`
  - use only after review if the source does not disclose a usable view

For themes:

- use `positive` when the theme is presented as a source of opportunity or structural support
- use `mixed` when the theme is both investable and a named risk
- use `negative` when the theme is discussed mainly as a threat

## Evidence Table Rules

`positioning_evidence.csv` is the audit trail.

- One row can represent one quote, one bullet, or one short passage.
- Multiple evidence rows can point to the same `topic_id`.
- Use the evidence table to preserve nuance before choosing the final normalized `view`.

## Examples

- `We prefer European small caps to crowded U.S. mega-cap winners`
  - `equities_geography_europe = positive`
  - `equities_size_small_cap = positive`
  - `why = valuation catch-up and under-ownership`

- `Carry still dominates, with euro IG preferred and HY only selective`
  - `fixed_income_credit_quality_investment_grade = positive`
  - `fixed_income_credit_quality_high_yield = mixed`

- `The dollar should soften while gold remains a hedge`
  - `currencies_usd = negative`
  - `commodities_gold = positive`

- `AI remains a structural opportunity but bubble risk is rising`
  - `themes_ai = mixed`

## Scope Discipline

This foundation is for Step 2 baseline positioning and themes only.

Do not expand the topic grid unless the new topic appears repeatedly across the corpus or is required by the brief. If the scope changes, update this codebook before changing the CSV templates.
