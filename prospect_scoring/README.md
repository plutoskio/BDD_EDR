# Prospect Scoring Engine

This folder contains a fully transparent `client x fund` scoring engine built on top of [CRM_2025.xlsx](/Users/milo/Desktop/BDD_EDR/CRM_2025.xlsx).

Its purpose is simple:

- rank which commercial relationships matter most to `defend` for a given fund
- rank which existing EdRAM relationships are best suited for `cross-sell`
- rank which existing relationships are best suited for a `new allocation`

This is a `sales-prioritization tool`, not a predictive machine-learning model.

The current build has already been run on the repo CRM and produced:

- `946` scored client keys
- `35` funds
- `33,110` client-fund score rows

## Why This Exists

The original D3 logic in this repo identifies which funds should be pushed in a given market. That is useful, but it is still one step away from field execution.

This scoring layer answers the next question:

`For each fund, which client relationship should Sales call first, and why?`

That is what makes it operational.

## Design Choice: Rules-Based, Not Machine Learning

The engine is intentionally rules-based.

That choice is deliberate for three reasons:

1. The CRM file is a `position snapshot`, not a historical conversion dataset.
There is no explicit label such as:
- won pitch
- lost pitch
- subscription amount
- redemption probability
- meeting outcome

2. Sales needs explainability.
A jury, Product team, or Sales head can challenge a score. A weighted score with visible inputs is defendable. A black-box model would not be.

3. The real goal is prioritization, not prediction.
This engine ranks where Sales should focus first using observable commercial fit, channel fit, installed base, and whitespace.

## Folder Contents

- [build_scores.py](/Users/milo/Desktop/BDD_EDR/prospect_scoring/build_scores.py)
  The end-to-end script that parses the Excel file, builds client profiles, computes scores, and writes outputs.
- [fund_taxonomy.json](/Users/milo/Desktop/BDD_EDR/prospect_scoring/fund_taxonomy.json)
  Manual taxonomy for the current fund universe.
- [outputs/fund_taxonomy_resolved.csv](/Users/milo/Desktop/BDD_EDR/prospect_scoring/outputs/fund_taxonomy_resolved.csv)
  Final taxonomy actually used after merging manual entries with fallback inference.
- [outputs/client_fund_scores.csv](/Users/milo/Desktop/BDD_EDR/prospect_scoring/outputs/client_fund_scores.csv)
  The full matrix: every client key scored against every fund.
- [outputs/top_targets_by_fund_and_action.csv](/Users/milo/Desktop/BDD_EDR/prospect_scoring/outputs/top_targets_by_fund_and_action.csv)
  The top 25 relationships per fund and per action.
- [outputs/fund_score_summary.csv](/Users/milo/Desktop/BDD_EDR/prospect_scoring/outputs/fund_score_summary.csv)
  Per-fund score summary.
- [outputs/run_summary.json](/Users/milo/Desktop/BDD_EDR/prospect_scoring/outputs/run_summary.json)
  Basic run metadata.

## Unit of Analysis

The engine scores a `client key`, not just a raw CRM row.

The `client_key` is defined as:

`Business Relationship | Business Country | BR Segmentation`

That means the same institution can appear more than once if it operates through:

- different countries
- different commercial segments

This is intentional. In sales reality, a private-banking relationship in France is not the same call plan as an insurance own-account mandate in Switzerland.

## Input Data Used

Directly from the CRM:

- `Business Relationship`
- `Fund`
- `AUM (€)`
- `BR Segmentation`
- `Business Country`

Derived at client-key level:

- total installed EdRAM AUM
- number of holdings lines
- number of unique funds held
- average line size
- concentration ratio
- current exposure to each target fund
- current exposure by asset class
- current exposure by strategy tags

Derived at fund level:

- current installed base by country
- current installed base by segment
- current installed base by client

## Taxonomy Layer

Every fund is mapped to a transparent taxonomy:

- `asset_class`
  Example: `fixed_income`, `equity`, `multi_asset`, `alternatives`
- `role`
  Example: `core`, `relay`, `satellite`
- `complexity`
  A simple 1-5 scale
- `tags`
  Example: `carry`, `healthcare`, `france`, `technology`, `small_cap`, `target_maturity`

Why this matters:

- it lets the engine recognize whether a client already uses adjacent sleeves
- it allows `cross-sell` and `new allocation` to mean different things
- it keeps the scoring fund-specific instead of generic

### Fallback Behavior

If a new fund appears in the CRM and is not present in [fund_taxonomy.json](/Users/milo/Desktop/BDD_EDR/prospect_scoring/fund_taxonomy.json), the script falls back to keyword inference.

That fallback is only a safety net. The preferred approach is still to extend the manual taxonomy.

## The Three Scores

Each `client x fund` pair gets three separate scores.

### 1. Defend Score

Question:

`Which existing holders of this exact fund matter most to protect and deepen?`

The score is only non-zero when the client already holds the target fund.

Main drivers:

- current holding size in the target fund
- target fund share of wallet
- overall relationship strength
- wallet breadth
- channel fit
- country fit

Interpretation:

- high `Defend Score` means Sales should protect and expand an existing installed position

### 2. Cross-Sell Score

Question:

`Which existing EdRAM relationships do not hold this fund yet, but already look familiar with adjacent sleeves?`

The score is only non-zero when the client does not already hold the target fund.

Main drivers:

- channel fit
- country fit
- relationship strength
- adjacency to the target sleeve
- average ticket size
- wallet breadth

Interpretation:

- high `Cross-Sell Score` means the client already behaves like a plausible buyer of this type of fund

### 3. New Allocation Score

Question:

`Which existing relationships could open a fresh sleeve in this fund, even if they are not already active in adjacent products?`

The score is only non-zero when the client does not already hold the target fund.

Main drivers:

- channel fit
- country fit
- relationship strength
- average ticket size
- whitespace / freshness
- diversification headroom

Interpretation:

- high `New Allocation Score` means the relationship is commercially large enough and structurally suitable to add a genuinely new sleeve

## Exact Formulas

All scores are normalized on a `0-100` scale.

### Base Components

Before scoring the three actions, the engine computes a few reusable base signals.

#### Relationship Strength

`relationship_strength`

= `55%` log-scaled total relationship AUM  
+ `20%` log-scaled average line size  
+ `15%` log-scaled number of unique funds held  
+ `10%` diversification bonus from lower concentration

Why:

- larger installed wallets matter more commercially
- larger average tickets matter more than tiny shelf positions
- broader existing EdRAM usage makes execution easier
- extremely concentrated wallets get a small penalty

#### Channel Fit

`channel_fit`

= `65%` empirical segment fit  
+ `35%` complexity fit

Where:

- `empirical segment fit` checks whether the fund is over-indexed in that segment relative to the overall CRM
- `complexity fit` checks whether the client segment is structurally suitable for the fund's complexity

#### Country Fit

`country_fit`

= empirical over-indexing of the fund in that country relative to the whole CRM

This is not saying "the fund can only work there". It is a practical product-market-fit signal.

#### Adjacency

`adjacency`

= `55%` current exposure to the target asset class  
+ `45%` current exposure to the target fund's primary tags

This is the main cross-sell familiarity measure.

#### Freshness

`freshness`

= `1 - (65% target asset-class exposure + 35% target-tag exposure)`

This is the main new-allocation whitespace measure.

### Defend Score

Only active when the relationship already holds the target fund.

`Defend Score`

= `35%` current holding strength in the target fund  
+ `20%` target fund share of wallet  
+ `15%` relationship strength  
+ `10%` wallet breadth  
+ `10%` channel fit  
+ `10%` country fit

Interpretation:

- a high score means the existing holding is too important to ignore and Sales should protect or deepen it

### Cross-Sell Score

Only active when the relationship does not already hold the target fund.

`Cross-Sell Base`

= `25%` channel fit  
+ `10%` country fit  
+ `20%` relationship strength  
+ `25%` adjacency  
+ `10%` average ticket size  
+ `10%` wallet breadth

`Cross-Sell Score`

= `Cross-Sell Base x (35% + 65% x adjacency)`

Why the gate exists:

- if adjacency is low, the relationship may still be commercially interesting, but it should not rank like a natural cross-sell account

### New Allocation Score

Only active when the relationship does not already hold the target fund.

`New Allocation Base`

= `25%` channel fit  
+ `10%` country fit  
+ `25%` relationship strength  
+ `10%` average ticket size  
+ `20%` freshness  
+ `10%` diversification headroom

`New Allocation Score`

= `New Allocation Base x (35% + 65% x freshness)`

Why the gate exists:

- if a client is already saturated in the same sleeve, it should not rank as a top `new allocation` prospect even if it is large

## Why One Generic Score Would Be Wrong

The scoring is fund-specific by construction.

That matters because:

- `Financial Bonds` needs very different client logic from `Tricolore Convictions`
- `Healthcare` should not be pushed to the same channels, with the same rationale, as a target-maturity bond fund
- a relationship can be an excellent fixed-income prospect and a poor thematic-equity prospect at the same time

The taxonomy and adjacency logic are what prevent the engine from ranking every large client highly for every fund.

## Scoring Logic

The engine combines three families of signals:

### 1. Relationship Strength

This captures how commercially important the relationship already is.

Built from:

- total AUM
- average line size
- number of unique funds held
- concentration ratio

This is not enough on its own, but it is an essential base layer.

### 2. Product Fit

This captures whether the client profile looks structurally suited to the fund.

Built from:

- `segment fit`
  Derived empirically from how strongly the fund is already represented in that segment relative to the overall CRM
- `country fit`
  Derived empirically from how strongly the fund is already represented in that country relative to the whole CRM
- `complexity fit`
  Compares the fund's complexity level to the commercial segment's capacity

### 3. Installed-Base Structure

This captures whether the wallet already has:

- a large holding to defend
- adjacent sleeves that make cross-sell easier
- whitespace that makes a new allocation attractive

Built from:

- target fund holding
- target asset-class exposure
- target-tag exposure
- concentration
- breadth of the existing EdRAM wallet

## Important Caveat About "Relationships"

This engine scores `client keys`, not CRM rows.

That distinction matters because raw row counts can overstate the number of truly unique commercial relationships.

If you use this in a deck:

- prefer `client keys scored`
- or `commercial relationships`
- and avoid mixing that with raw holdings-line counts unless you say so explicitly

## How To Run

From the repo root:

```bash
python3 prospect_scoring/build_scores.py
```

No external Python packages are required. The parser uses only the standard library and reads the `.xlsx` file directly as zipped XML.

When the script runs successfully, it prints a short JSON summary and writes the same metadata to [outputs/run_summary.json](/Users/milo/Desktop/BDD_EDR/prospect_scoring/outputs/run_summary.json).

## Output Files

### 1. `client_fund_scores.csv`

This is the master matrix.

Each row is one `client_key x fund` pair.

Main columns:

- `client_key`
- `business_relationship`
- `country`
- `segment`
- `fund`
- `fund_asset_class`
- `fund_role`
- `current_target_aum_eur`
- `channel_fit_score`
- `country_fit_score`
- `relationship_strength_score`
- `adjacency_score`
- `freshness_score`
- `defend_score`
- `cross_sell_score`
- `new_allocation_score`
- `best_action`
- `best_score`
- `reason_1..reason_3`

### 2. `top_targets_by_fund_and_action.csv`

This is the usable sales shortlist.

For each fund and for each action:

- top 25 `Defend`
- top 25 `Cross-Sell`
- top 25 `New Allocation`

### 3. `fund_score_summary.csv`

This is the management view.

It shows for each fund:

- how many client keys were scored
- how many are already holders
- average score levels
- top score levels by action

## How To Use It In A Pitch

The cleanest framing is:

`We built a commercial prioritization engine that scores every client relationship against every fund across three actions: defend, cross-sell, and new allocation.`

That is much stronger than:

`We think Fund X is good for France.`

You can use the outputs in three ways:

1. `Fund-first`
Show the top targets for one flagship fund.

2. `Action-first`
Show how Sales should split effort between defend, cross-sell, and new allocation.

3. `Country-first`
Filter the master matrix to one country and build the local call plan from there.

## What This Does Not Do

This engine does not predict flows.

It does not know:

- past conversion rates by client
- meeting outcomes
- redemption behavior
- fee schedules
- competitor holdings inside each account

So the correct claim is:

`This ranks where Sales should focus first based on fit and installed-base evidence.`

Not:

`This predicts who will subscribe next.`

## Good Next Extensions

If you want to push this further later, the strongest upgrades would be:

1. Add explicit fund fees to convert opportunities into revenue scoring.
2. Add historical flows if available.
3. Add competitor-product mapping per fund.
4. Add country-specific score weight overrides.
5. Add a small front-end layer to filter by country, segment, and action.
