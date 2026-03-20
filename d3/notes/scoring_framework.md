# D3 Scoring Framework

Deliverable 3 should be built as a ranking model, not as five disconnected narratives.

## Objective

For each target country, rank EdRAM funds by commercial priority using a mix of macro fit and sales fit.

## Scoring Axes

Use a 1-5 scale on each axis.

### 1. Narrative Fit

Question:
Does the fund match the dominant local macro and positioning narrative?

Examples:

- Europe recovery and domestic catch-up: Europe equity, small-cap, or selective value exposure
- Sticky inflation but easing rates: carry, short-duration credit, financial bonds, hybrids
- Selective risk appetite with AI enthusiasm: Big Data or other technology-adjacent funds
- Defensive quality / resilience: healthcare or resilient multi-asset credit

### 2. Commercial Traction

Question:
Does the CRM show this fund already has adoption in the target country?

Use both:

- installed AUM
- relationship count / row count

Interpretation:

- high traction = easier scaling story
- low traction = only interesting if the narrative fit is especially strong

### 3. Channel Fit

Question:
Is the fund suited to the dominant local client segments?

Examples:

- private banking markets can absorb more sophisticated thematic or credit stories
- retail-led markets need simpler and more scalable messages
- platform-heavy markets favor liquid, easy-to-screen products
- insurance / unit-link channels need product suitability and packaging discipline

### 4. Strategic White Space

Question:
Is this a defend-the-base recommendation or an underpenetrated opportunity?

Interpretation:

- `5` = strong opening where macro fit is high and current penetration is still low
- `3` = obvious but necessary recommendation with existing traction
- `1` = low incremental value beyond what is already concentrated

### 5. Sales Simplicity

Question:
Can a country sales lead explain the product in one sentence tied to the local narrative?

This matters because a case-winning answer should be usable in the field.

## Output Structure Per Country

Each country should end with three ranked recommendations:

- `Scale Now`
  - strongest combination of fit and immediate commercial plausibility
- `Strategic Bet`
  - best differentiated opportunity with credible upside
- `Challenger`
  - smaller or more selective idea that shows judgment beyond the obvious

## KPI Template

Each recommendation should carry 2-3 KPIs chosen from:

- current installed AUM in country
- current relationship count in country
- share of country book represented by the fund
- share of target segment already exposed to the fund
- number of reachable accounts in the target segment
- expected cross-sell pool from adjacent product holdings

## Rule

No recommendation should survive if it has only macro logic or only CRM logic.

We need both.
